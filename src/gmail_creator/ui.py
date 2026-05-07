from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table
from rich.text import Text

from src.gmail_creator import __version__
from src.gmail_creator.stats import get_active_accounts, get_last_creation, get_total_accounts

console = Console()


def print_banner() -> None:
    title = Text()
    title.append("Gmail Creator Pro", style="bold blue")
    title.append(f" v{__version__}", style="yellow")
    banner = Panel(title, subtitle="Automated Gmail Account Creator", width=60)
    console.print(banner)
    console.print()


def print_menu() -> None:
    table = Table(title="Menu Options", show_header=False, border_style="cyan")
    table.add_column("Option", style="bold yellow", width=8)
    table.add_column("Description")
    table.add_row("1", "Create Gmail Accounts")
    table.add_row("2", "View Statistics")
    table.add_row("3", "Settings")
    table.add_row("4", "View Saved Accounts")
    table.add_row("5", "Exit")
    console.print(table)
    console.print()


def print_stats() -> None:
    total = get_total_accounts()
    active = get_active_accounts()
    last = get_last_creation()
    table = Table(title="Statistics", border_style="green")
    table.add_column("Metric", style="bold cyan")
    table.add_column("Value")
    table.add_row("Total Accounts Created", str(total))
    table.add_row("Active Accounts", str(active))
    table.add_row("Last Creation", last or "N/A")
    console.print(table)
    console.print()


def print_accounts() -> None:
    from src.gmail_creator.stats import load_accounts

    accounts = load_accounts()
    if not accounts:
        console.print("[yellow]No accounts found.[/yellow]")
        console.print()
        return
    table = Table(title="Saved Accounts", border_style="blue")
    table.add_column("#", style="dim")
    table.add_column("Email", style="cyan")
    table.add_column("Created", style="green")
    table.add_column("Status")
    for i, acc in enumerate(accounts, 1):
        status_style = "green" if acc.get("status") == "active" else "red"
        table.add_row(
            str(i),
            acc.get("email", ""),
            acc.get("created_at", ""),
            f"[{status_style}]{acc.get('status', '')}[/{status_style}]",
        )
    console.print(table)
    console.print()


def print_account_created(account: dict[str, Any]) -> None:
    console.print(
        f"[green]Account created:[/green] {account['email']}",
    )


def print_error(msg: str) -> None:
    console.print(f"[red]Error:[/red] {msg}")


def print_warning(msg: str) -> None:
    console.print(f"[yellow]Warning:[/yellow] {msg}")


def print_info(msg: str) -> None:
    console.print(f"[cyan]{msg}[/cyan]")


def input_number(prompt: str = "Enter number: ") -> int:
    try:
        return int(console.input(f"[bold]{prompt}[/bold]"))
    except ValueError:
        return 0


def create_progress() -> Progress:
    return Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
