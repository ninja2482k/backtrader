import shutil
from datetime import datetime
from typing import Dict, Any, List
import pyfiglet
from rich.console import Console
from rich.table import Table
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


def _prompt_with_default(console: Console, prompt: str, default: str) -> str:
    console.print(f"{prompt} [dim](default: {default})[/dim]: ", end="")
    user_input = input().strip()
    return user_input if user_input else default


def _prompt_select(console: Console, prompt: str, options: List[str], default_index: int = 0) -> str:
    console.print(f"\n[bold]{prompt}[/bold]")
    for idx, option in enumerate(options, start=1):
        default_marker = " [dim](default)" if (idx - 1) == default_index else ""
        console.print(f"  {idx}. {option}{default_marker}")
    console.print(f"Select 1-{len(options)}: ", end="")
    choice_str = input().strip()
    if choice_str.isdigit():
        choice = int(choice_str)
        if 1 <= choice <= len(options):
            return options[choice - 1]
    return options[default_index]


def _prompt_float(console: Console, prompt: str, default: float) -> float:
    console.print(f"{prompt} [dim](default: {default})[/dim]: ", end="")
    raw = input().strip()
    if raw == "":
        return default
    try:
        return float(raw)
    except ValueError:
        console.print("[red]Invalid number. Using default.[/red]")
        return default


def _prompt_percent(console: Console, prompt: str, default_percent: float) -> float:
    console.print(f"{prompt} [dim](default: {default_percent}%) [/dim]: ", end="")
    raw = input().strip()
    if raw == "":
        return default_percent / 100.0
    try:
        normalized = raw.replace("%", "").strip()
        value = float(normalized)
        # User entered percent scale; convert to fraction
        return value / 100.0
    except ValueError:
        console.print("[red]Invalid percent. Using default.[/red]")
        return default_percent / 100.0


def _prompt_date(console: Console, prompt: str, default: str | None = None) -> str | None:
    suffix = f" [dim](YYYY-MM-DD{' | Enter to skip' if default is None else f' | default: {default}'})[/dim]"
    console.print(f"{prompt}{suffix}: ", end="")
    raw = input().strip()
    if raw == "":
        return default
    try:
        # Validate format
        datetime.strptime(raw, "%Y-%m-%d")
        return raw
    except ValueError:
        console.print("[red]Invalid date. Please use YYYY-MM-DD. Leaving empty.[/red]")
        return default


def _prompt_bool(console: Console, prompt: str, default: bool) -> bool:
    default_label = "y" if default else "n"
    console.print(f"{prompt} [dim](y/n, default: {default_label})[/dim]: ", end="")
    raw = input().strip().lower()
    if raw == "":
        return default
    return raw in {"y", "yes", "true", "1"}


def _collect_backtest_parameters(console: Console) -> Dict[str, Any]:
    # Choices
    timeframe_options = ["1m", "5m", "15m", "1h", "4h", "1d"]
    strategy_options = [
        "MovingAverageCross",
        "RSIReversion",
        "Breakout",
    ]

    # Prompts
    console.print("")
    symbol = _prompt_with_default(console, "Enter Symbol", "AAPL")
    timeframe = _prompt_select(console, "Select Timeframe", timeframe_options, default_index=5)
    start_date = _prompt_date(console, "Enter Start Date", default=None)
    end_date = _prompt_date(console, "Enter End Date", default=None)
    strategy = _prompt_select(console, "Select Strategy", strategy_options, default_index=0)
    starting_capital = _prompt_float(console, "Starting Capital", 10_000.0)
    risk_per_trade_fraction = _prompt_percent(console, "Risk Per Trade (%)", 1.0)
    stop_loss_fraction = _prompt_percent(console, "Stop Loss (%)", 2.0)
    take_profit_fraction = _prompt_percent(console, "Take Profit (%)", 4.0)
    slippage = _prompt_float(console, "Slippage (per unit or % of price if your engine expects it)", 0.0)
    commission_fraction = _prompt_percent(console, "Commission (%)", 0.0)
    show_chart = _prompt_bool(console, "Show Chart?", True)
    save_results = _prompt_bool(console, "Save Results?", False)

    params: Dict[str, Any] = {
        "symbol": symbol,
        "timeframe": timeframe,
        "start_date": start_date,
        "end_date": end_date,
        "strategy": strategy,
        "starting_capital": starting_capital,
        "risk_per_trade_fraction": risk_per_trade_fraction,
        "stop_loss_fraction": stop_loss_fraction,
        "take_profit_fraction": take_profit_fraction,
        "slippage": slippage,
        "commission_fraction": commission_fraction,
        "show_chart": show_chart,
        "save_results": save_results,
    }
    return params


def _render_parameters_summary(console: Console, params: Dict[str, Any]) -> None:
    table = Table(title="Backtest Parameters", show_header=True, header_style="bold blue")
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    def pct(frac: float) -> str:
        return f"{frac * 100:.2f}%"

    rows = [
        ("Symbol", params["symbol"]),
        ("Timeframe", params["timeframe"]),
        ("Start Date", params["start_date"] or "(none)"),
        ("End Date", params["end_date"] or "(none)"),
        ("Strategy", params["strategy"]),
        ("Starting Capital", f"{params['starting_capital']:.2f}"),
        ("Risk Per Trade", pct(params["risk_per_trade_fraction"])),
        ("Stop Loss", pct(params["stop_loss_fraction"])),
        ("Take Profit", pct(params["take_profit_fraction"])),
        ("Slippage", str(params["slippage"])),
        ("Commission", pct(params["commission_fraction"])),
        ("Show Chart", "Yes" if params["show_chart"] else "No"),
        ("Save Results", "Yes" if params["save_results"] else "No"),
    ]
    for field, value in rows:
        table.add_row(field, value)

    console.print("")
    console.print(table)


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

    params = _collect_backtest_parameters(console)
    _render_parameters_summary(console, params)

    console.print("\n[bold green]Parameters collected.[/bold green] This is where the backtest would start.")
    console.print("\nPress Enter to return...", style="dim")
    input()


if __name__ == "__main__":
    run_core_engine()