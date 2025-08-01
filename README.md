# Tau Lang TUI Wrapper

This project is a multi-panel Terminal User Interface (TUI) for interacting with the **[Tau-lang REPL](https://github.com/IDNI/tau-lang)**. It provides a user-friendly environment with separate panels for REPL interaction, command history, and a detailed debug log.

* **Multi-Panel Layout**: A clean interface with dedicated, scrollable panels for REPL output, command history, and a debug log.
* **System Stats**: A live display of your current CPU and RAM usage.
* **Debug & Timing**: The debug panel shows a timestamped log of every command sent to the Tau REPL and every response received, including execution time.
* **Themed Interface**: Styled with the popular Catppuccin color theme for a modern look.

---

## Requirements

* **Python 3.7+**
* The compiled **`tau` executable** from the [Tau-lang repository](https://github.com/IDNI/tau-lang).

---

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Install the required Python libraries:**
    This project depends on `textual` for the interface and `psutil` for system stats.
    ```bash
    pip install textual psutil
    ```

---

## Configuration & Usage

To run the TUI, the script must know where to find the `tau` executable. There are several ways to configure this, listed from highest to lowest priority.

### Option 1: Command-Line Argument (Highest Priority)

Provide the path directly when you run the script. This method overrides all others.

```bash
python tau_tui.py --tau-path C:\path\to\your\tau.exe
```

### Option 2: Configuration File (config.ini)

For a more permanent setting, you can edit the config.ini file.

Open config.ini in a text editor.

Set the value of TauExecutable to the full path of your tau executable.

Important: Do not use quotes around the path.

### Option 3: Automatic Detection (Lowest Priority)

If no other configuration is provided, the script will automatically look for tau or tau.exe in the same directory as the script itself.

---

## Running the Application

Once configured, simply run the script from your terminal:

```bash
python tau_tui.py
```
