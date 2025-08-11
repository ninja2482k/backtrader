import shutil
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


def run_core_engine() -> None:
    console = Console()
    # Blue palette to match the main menu
    colors = [
        "#0d47a1",
        "#1976d2",
        "#2196f3",
        "#64b5f6",
        "#90caf9",
        "#42a5f5",
        "#1e88e5",
        "#1565c0",
    ]
    banner = build_banner_text("Core Engine", colors)
    console.clear()
    console.print(banner)
    console.print("[bold blue]Backtrading Core Engine[/bold blue]")
    console.print("\n[bold blue]This is a placeholder for the core backtesting engine interface.[/bold blue]")
    console.print("\nPress Enter to return...", style="dim")
    input()


if __name__ == "__main__":
    run_core_engine()


