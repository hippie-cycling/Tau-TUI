import asyncio
import re
import time
import os
import argparse
import configparser
from datetime import datetime
from pathlib import Path

import psutil
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Input, RichLog, Static

# --- Configuration Hierarchy ---
def find_tau_executable():
    """Finds the Tau executable using a hierarchy of methods."""
    parser = argparse.ArgumentParser(description="A TUI wrapper for the Tau-lang REPL.")
    parser.add_argument("--tau-path", help="Path to the tau executable.")
    args = parser.parse_args()
    if args.tau_path and Path(args.tau_path).is_file():
        return args.tau_path

    config = configparser.ConfigParser()
    if config.read('config.ini') and 'Paths' in config and 'TauExecutable' in config['Paths']:
        path_from_config = config['Paths']['TauExecutable']
        if path_from_config and Path(path_from_config).is_file():
            return path_from_config

    search_paths = [Path("./tau"), Path("./tau.exe")]
    for path in search_paths:
        if path.is_file():
            return str(path)
    
    return None

TAU_EXECUTABLE_PATH = find_tau_executable()

def strip_ansi_codes(text: str) -> str:
    """Removes ANSI escape codes from a string."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

class StatsDisplay(Static):
    """A widget to display CPU and RAM usage."""
    def on_mount(self) -> None:
        self.set_interval(1, self.update_stats)

    def update_stats(self) -> None:
        self.update(f" CPU: {psutil.cpu_percent():2.1f}%    RAM: {psutil.virtual_memory().percent:2.1f}%")

class TauTUI(App):
    """A multi-panel TUI for the Tau-lang REPL."""

    CSS_PATH = "tau_tui.css"
    BINDINGS = [("ctrl+c", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        if not TAU_EXECUTABLE_PATH:
            yield Static("[bold red]Error: Tau executable not found.[/]\n\nPlease configure the path in 'config.ini' or use the --tau-path argument.", id="error-message")
            return
            
        yield Header()
        yield StatsDisplay(id="stats-display")
        
        # --- NEW HEADER WIDGET IS HERE ---
        yield Static("[b]Tau TUI[/] [dim]v1.0[/]                                [dim]https://github.com/hippie-cycling/Tau-TUI[/]", id="app-header")

        with Horizontal(id="main-container"):
            with Vertical(id="repl-container"):
                with Container(id="repl-border", classes="panel-container"):
                    yield Static("REPL Output", classes="title")
                    yield RichLog(id="repl-log", wrap=True, markup=True)
                yield Input(placeholder="Enter Tau command...")
            
            with Vertical(id="right-column"):
                with Container(id="history-container", classes="panel-container"):
                    yield Static("History", classes="title")
                    yield RichLog(id="history-log", wrap=True, markup=True)
                with Container(id="debug-container", classes="panel-container"):
                    yield Static("Debug Log", classes="title")
                    yield RichLog(id="debug-log", wrap=True, markup=True)
        yield Footer()

    def on_mount(self) -> None:
        if not TAU_EXECUTABLE_PATH:
            return
            
        self.repl_log = self.query_one("#repl-log", RichLog)
        self.debug_log = self.query_one("#debug-log", RichLog)
        self.history_log = self.query_one("#history-log", RichLog)
        self.run_worker(self.run_tau_process, exclusive=True)
        self.query_one(Input).focus()

    async def run_tau_process(self) -> None:
        try:
            self.process = await asyncio.create_subprocess_exec(
                TAU_EXECUTABLE_PATH,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
            self.repl_log.write("[#ded1c2]▶ Tau REPL process started...[/]")
            self.debug_log.write(f"[{datetime.now().time()}] [#ded1c2 bold]▶ PROCESS STARTED[/]")

            while self.process.returncode is None:
                line_bytes = await self.process.stdout.readline()
                if not line_bytes: break
                
                duration = 0.0
                if hasattr(self, "command_start_time"):
                    duration = time.monotonic() - self.command_start_time
                    del self.command_start_time

                cleaned_line = strip_ansi_codes(line_bytes.decode(errors="replace").strip())
                
                self.repl_log.write(cleaned_line)
                self.debug_log.write(f"[{datetime.now().time()}] [#89b4fa bold]◀ RECV[/] [dim]({duration:.4f}s): {cleaned_line}[/]")

        except FileNotFoundError:
            self.repl_log.write(f"[#f38ba8]Error: Tau executable not found at '{TAU_EXECUTABLE_PATH}'.[/]")
        except Exception as e:
            self.repl_log.write(f"[#f38ba8]An unexpected error occurred: {e}[/]")
        finally:
            self.debug_log.write(f"[{datetime.now().time()}] [#fab387 bold]■ PROCESS FINISHED[/]")

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        command = message.value

        if hasattr(self, "process") and self.process.returncode is None:
            self.repl_log.write(f"[#cba6f7]> {command}[/]")
            self.history_log.write(f"[#ded1c2]» {command}[/]")
            self.debug_log.write(f"[{datetime.now().time()}] [#ded1c2 bold]▶ SEND[/]: {command}")
            
            self.command_start_time = time.monotonic()
            
            self.process.stdin.write((command + "\n").encode())
            await self.process.stdin.drain()
            message.input.clear()
        else:
            self.repl_log.write("[#f38ba8]Tau process is not running.[/]")

if __name__ == "__main__":
    app = TauTUI()
    app.run()