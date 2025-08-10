import platform
import socket
import importlib
import os
from rich.console import Console

console = Console()

def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except Exception:
        return False

def check_requirements():
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    # Read package names from requirements.txt
    if not os.path.exists(req_path):
        return []
    with open(req_path) as f:
        required = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    # Check if each package can be imported
    results = []
    for pkg in required:
        try:
            importlib.import_module(pkg)
            results.append((pkg, True))
        except ImportError:
            results.append((pkg, False))
    return results

def run_diagnostics():
    console.print("\n[bold blue][ System Check Started ]\n")
    # Python version
    console.print(f"[bold blue]✔ Python version: [bold green]{platform.python_version()}")

    # Check required packages
    pkg_results = check_requirements()
    all_installed = all(ok for pkg, ok in pkg_results)
    if all_installed:
        console.print(f"[bold blue]✔ Required packages installed: [bold green]OK")
    else:
        console.print(f"[bold blue]✖ Required packages installed: [bold red]FAILED")

    # Internet connection
    if check_internet():
        console.print(f"[bold blue]✔ Internet connection: [bold green]OK")
    else:
        console.print(f"[bold blue]✖ Internet connection: [bold red]FAILED")

    console.print("\n[bold blue]====================================\n")

if __name__ == "__main__":
    run_diagnostics()
