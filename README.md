# Tau Lang TUI Wrapper

This project is a sophisticated, multi-panel Terminal User Interface (TUI) for interacting with the **[Tau-lang REPL](https://github.com/IDNI/tau-lang)**. It provides a user-friendly environment with separate panels for REPL interaction, command history, and a detailed debug log.

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

## How to Use

To run the TUI, you must first tell it where to find the `tau` executable. You can do this in one of three ways (from highest to lowest priority):

### Option 1: Command-Line Argument (Recommended for temporary use)

Provide the path directly when you run the script.

```bash
python tau_tui.py --tau-path /path/to/your/tau
    ```