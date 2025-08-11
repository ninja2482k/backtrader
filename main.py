import shutil
import time
import sys
import subprocess
import pyfiglet
from rich.console import Console
from rich.text import Text

def build_banner_text(title: str, colors: list[str]) -> Text:
    ascii_banner = pyfiglet.figlet_format(title)
    banner_lines = ascii_banner.splitlines()
    term_width = shutil.get_terminal_size((80, 20)).columns
    max_len = max(len(line) for line in banner_lines)
    pad_width = max(term_width, max_len)
    text = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        padded_line = line.center(pad_width)
        text.append(padded_line + "\n", style=f"bold {color}")
    return text


def print_menu(console: Console, options: list[str], colors: list[str]) -> None:
    for idx, option in enumerate(options, 1):
        color = colors[idx % len(colors)]
        menu_text = Text(f"{idx}. {option}", style=f"bold {color}")
        console.print(menu_text)


def prompt_choice(console: Console, num_options: int) -> str:
    console.print(f"\nSelect an option (1-{num_options}) or press Enter to exit: ", end="")
    return input().strip()


def pause_and_return(console: Console, banner_text: Text) -> None:
    console.print("\nPress Enter to return to the menu...", style="dim")
    input()
    console.clear()
    console.print(banner_text)


def main():
    console = Console()

    # Colors and banner
    blues = [
        "#0d47a1",
        "#1976d2",
        "#2196f3",
        "#64b5f6",
        "#90caf9",
        "#42a5f5",
        "#1e88e5",
        "#1565c0",
    ]
    banner_text = build_banner_text("Backtrader", blues)
    console.print(banner_text)

    # Menu config
    menu_options = [
        "Start Backtest",
        "View Results",
        "Load Historical Data",
        "Settings",
        "Diagnostics",
    ]
    menu_messages = {
        "1": "Start Backtest selected!",
        "2": "View Results selected!",
        "3": "Load Historical Data selected!",
        "4": "Settings selected!",
        "5": "Diagnostics selected!",
    }

    while True:
        # Render menu
        print_menu(console, menu_options, blues)

        # Read choice
        choice = prompt_choice(console, len(menu_options))
        if choice == "":
            time.sleep(2)
            break

        # Handle selection
        if choice in menu_messages:
            console.clear()
            console.print(menu_messages[choice])

            if choice == "1":
                subprocess.run([sys.executable, "core_engine.py"])
                pause_and_return(console, banner_text)
                continue

            if choice == "5":
                subprocess.run([sys.executable, "diagnostic.py"])
                pause_and_return(console, banner_text)
                continue

            pause_and_return(console, banner_text)
            continue

        console.print(f"Invalid option. Please select a number between 1 and {len(menu_options)}.\n")

if __name__ == "__main__":
    main()