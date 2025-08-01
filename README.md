This project is a sophisticated, multi-panel Terminal User Interface (TUI) for interacting with the Tau-lang REPL. It provides a user-friendly environment with separate panels for REPL interaction, command history, and a detailed debug log.

### Features

Multi-Panel Layout: A clean interface with dedicated, scrollable panels for REPL output, command history, and a debug log.

System Stats: A live display of your current CPU and RAM usage.

Debug & Timing: The debug panel shows a timestamped log of every command sent to the Tau REPL and every response received, including execution time.

Themed Interface: Styled with the popular Catppuccin color theme for a modern look.

Requirements
Python 3.7+

The compiled tau executable from the Tau-lang repository.

Installation
Clone the repository:

Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install the required Python libraries:
This project depends on textual for the interface and psutil for system stats.

Bash

pip install textual psutil
How to Use
Configure the Executable Path:
Open the tau_tui.py file and update the TAU_EXECUTABLE_PATH variable to point to the location of your tau executable.

Python

# tau_tui.py
TAU_EXECUTABLE_PATH = '/path/to/your/tau/executable' 
Run the Application:
Execute the Python script from your terminal.

Bash

python tau_tui.py