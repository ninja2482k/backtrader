
import shutil
import time
import sys
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

def main():
    # Generate and print the ASCII art banner
    ascii_banner = pyfiglet.figlet_format("Backtrader")
    console = Console()

    # Blue gradient colors
    blues = ["#0d47a1", "#1976d2", "#2196f3", "#64b5f6", "#90caf9", "#42a5f5", "#1e88e5", "#1565c0"]
    banner_lines = ascii_banner.splitlines()
    term_width = shutil.get_terminal_size((80, 20)).columns
    max_len = max(len(line) for line in banner_lines)
    pad_width = max(term_width, max_len)
    text = Text()
    for i, line in enumerate(banner_lines):
        color = blues[i % len(blues)]
        padded_line = line.center(pad_width)
        text.append(padded_line + "\n", style=f"bold {color}")
    console.print(text)

    # Menu options and their corresponding messages
    menu_dict = {
        "1": "Start Backtest selected!",
        "2": "View Results selected!",
        "3": "Load Historical Data selected!",
        "4": "Settings selected!",
        "5": "Diagnostics selected!",
        "6": "Exit selected!"
    }
    menu_options = [
        "Start Backtest",
        "View Results",
        "Load Historical Data",
        "Settings",
        "Diagnostics",
        "Exit"
    ]
    while True:
        # Print menu options with color
        for idx, option in enumerate(menu_options, 1):
            color = blues[idx % len(blues)]
            menu_text = Text(f"{idx}. {option}", style=f"bold {color}")
            console.print(menu_text)
        # Prompt user for input
        console.print(f"\nSelect an option (1-{len(menu_options)}): ", end="")
        choice = input().strip()
        # Handle menu selection
        if choice in menu_dict:
            console.print(f"{menu_dict[choice]}\n")
            if choice == "5":
                import subprocess
                subprocess.run([sys.executable, "diagnostic.py"])
            if choice == str(len(menu_options)):
                time.sleep(1)
                break
        else:
            console.print(f"Invalid option. Please select a number between 1 and {len(menu_options)}.\n")

if __name__ == "__main__":
    main()