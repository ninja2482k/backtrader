import platform
import socket
import importlib
import os
import shutil
from typing import List, Tuple
import pyfiglet
from rich.console import Console
from rich.text import Text

console = Console()


def check_internet() -> bool:
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except Exception:
        return False


def check_requirements() -> List[Tuple[str, bool]]:
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if not os.path.exists(req_path):
        return []
    with open(req_path) as f:
        required = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    results: List[Tuple[str, bool]] = []
    for pkg in required:
        try:
            importlib.import_module(pkg)
            results.append((pkg, True))
        except ImportError:
            results.append((pkg, False))
    return results


def print_header(c: Console) -> None:
    c.print("\n[bold blue][ System Check Started ]\n")


def print_python_version(c: Console) -> None:
    c.print(f"[bold blue]✔ Python version: [bold green]{platform.python_version()}")


def print_requirements_status(c: Console, results: List[Tuple[str, bool]]) -> None:
    all_installed = all(ok for _, ok in results)
    if all_installed:
        c.print(f"[bold blue]✔ Required packages installed: [bold green]OK")
    else:
        c.print(f"[bold blue]✖ Required packages installed: [bold red]FAILED")


def print_internet_status(c: Console) -> None:
    if check_internet():
        c.print(f"[bold blue]✔ Internet connection: [bold green]OK")
    else:
        c.print(f"[bold blue]✖ Internet connection: [bold red]FAILED")


def print_footer(c: Console) -> None:
    c.print("\n[bold blue]====================================\n")


def run_diagnostics() -> None:
    # Blue palette to match the main UI
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

    banner_text = build_banner_text("Diagnostics", blues)
    console.print(banner_text)
    print_header(console)
    print_python_version(console)
    pkg_results = check_requirements()
    print_requirements_status(console, pkg_results)
    print_internet_status(console)
    print_footer(console)


def build_banner_text(title: str, colors: List[str]) -> Text:
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

if __name__ == "__main__":
    run_diagnostics()
