import platform
import socket
import importlib
import os
from typing import List, Tuple
from rich.console import Console

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
    print_header(console)
    print_python_version(console)
    pkg_results = check_requirements()
    print_requirements_status(console, pkg_results)
    print_internet_status(console)
    print_footer(console)

if __name__ == "__main__":
    run_diagnostics()
