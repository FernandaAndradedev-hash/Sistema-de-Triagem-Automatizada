"""
Interface CLI do MailMind com Rich.
"""
import logging
import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from pipeline import run_triage, save_report
from email_data import get_all_emails

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
console = Console()

# Cores por urgência
URGENCY_COLORS = {
    "alta": "bold red",
    "media": "bold yellow",
    "baixa": "bold blue",
}

# Emojis por categoria
CATEGORY_EMOJIS = {
    "proposta": "💼",
    "reuniao": "📅",
    "financeiro": "💰",
    "reclamacao": "⚠️",
    "feedback": "⭐",
    "informacao": "❓",
    "interno": "🏢",
    "spam": "🗑️",
}


def print_banner():
    console.print(Panel.fit(
        "[bold cyan]MailMind[/bold cyan]\n"
        "[dim]Triagem automática de e-mails — Nexus Consultoria[/dim]",
        border_style="cyan",
    ))


def print_results_table(results):
    """Exibe tabela resumida de todos os e-mails."""
    table = Table(
        title="Resultado da Triagem",
        box=box.ROUNDED,
        show_lines=True,
    )

    table.add_column("#", style="dim", width=4)
    table.add_column("Remetente", style="bold")
    table.add_column("Assunto")
    table.add_column("Categoria", justify="center")
    table.add_column("Urgência", justify="center")
    table.add_column("Status", justify="center")

    for r in results:
        emoji = CATEGORY_EMOJIS.get(r.category, "📧")
        urgency_style = URGENCY_COLORS.get(r.urgency, "white")
        status = "❌ Erro" if r.error else "✅ OK"

        table.add_row(
            r.email.id,
            r.email.sender_name,
            r.email.subject[:50] + ("..." if len(r.email.subject) > 50 else ""),
            f"{emoji} {r.category}",
            f"[{urgency_style}]{r.urgency.upper()}[/{urgency_style}]",
            status,
        )

    console.print(table)


def print_email_detail(result):
    """Exibe detalhes completos de um e-mail triado."""
    urgency_style = URGENCY_COLORS.get(result.urgency, "white")
    emoji = CATEGORY_EMOJIS.get(result.category, "📧")

    console.print(Panel(
        f"[bold]De:[/bold] {result.email.sender_name} <{result.email.sender_email}>\n"
        f"[bold]Assunto:[/bold] {result.email.subject}\n"
        f"[bold]Recebido:[/bold] {result.email.received_at}\n\n"
        f"[bold]Categoria:[/bold] {emoji} {result.category}\n"
        f"[bold]Urgência:[/bold] [{urgency_style}]{result.urgency.upper()}[/{urgency_style}]\n\n"
        f"[bold]Resumo:[/bold]\n{result.summary}\n\n"
        f"[bold]Resposta sugerida:[/bold]\n[dim]{result.suggested_reply}[/dim]",
        title=f"E-mail #{result.email.id}",
        border_style="cyan",
    ))


def print_summary(results):
    """Exibe resumo estatístico."""
    total = len(results)
    errors = sum(1 for r in results if r.error)
    alta = sum(1 for r in results if r.urgency == "alta" and not r.error)
    media = sum(1 for r in results if r.urgency == "media" and not r.error)
    baixa = sum(1 for r in results if r.urgency == "baixa" and not r.error)

    console.print(Panel(
        f"[bold]Total de e-mails:[/bold] {total}\n"
        f"[bold red]Urgência alta:[/bold red] {alta}\n"
        f"[bold yellow]Urgência média:[/bold yellow] {media}\n"
        f"[bold blue]Urgência baixa:[/bold blue] {baixa}\n"
        f"[bold red]Erros:[/bold red] {errors}",
        title="📊 Resumo",
        border_style="green",
    ))


def main():
    print_banner()

    # Modo detalhe: python cli.py --detail
    show_detail = "--detail" in sys.argv

    console.print(f"\n[dim]Triando {len(get_all_emails())} e-mails...[/dim]\n")

    results = run_triage()

    print_results_table(results)
    console.print()
    print_summary(results)

    if show_detail:
        console.print("\n[bold]Detalhes de cada e-mail:[/bold]\n")
        for result in results:
            if not result.error:
                print_email_detail(result)
                console.print()

    # Salva relatório
    filepath = save_report(results)
    console.print(f"\n[dim]Relatório salvo em: {filepath}[/dim]")


if __name__ == "__main__":
    main()