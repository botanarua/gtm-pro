"""CLI entry point for the Legal Demand Planner."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from legal_demand_planner.models import BenefitInput, PlannerOutput
from legal_demand_planner.pipeline import run_pipeline

console = Console()


def _load_inputs(paths: tuple[str, ...]) -> list[BenefitInput]:
    """Carrega inputs de arquivos JSON."""
    inputs = []
    for path in paths:
        with open(path) as f:
            data = json.load(f)
        if isinstance(data, list):
            inputs.extend(BenefitInput(**item) for item in data)
        else:
            inputs.append(BenefitInput(**data))
    return inputs


def _print_summary(output: PlannerOutput) -> None:
    """Imprime resumo formatado no terminal."""
    console.print()
    console.print(
        Panel.fit(
            "[bold]Legal Demand Planner — Resultado da Análise[/bold]",
            border_style="blue",
        )
    )

    # Ranking
    console.print()
    table = Table(title="Ranking de Benefícios", show_lines=True)
    table.add_column("#", justify="center", style="bold")
    table.add_column("Benefício", style="cyan")
    table.add_column("Score", justify="center")
    table.add_column("Diagnóstico", justify="center")
    table.add_column("CAC Blended", justify="right")
    table.add_column("Orçamento Rec.", justify="right")

    label_styles = {
        "testar": "[bold green]TESTAR[/bold green]",
        "testar_com_cautela": "[bold yellow]TESTAR COM CAUTELA[/bold yellow]",
        "nao_testar": "[bold red]NÃO TESTAR[/bold red]",
    }

    for r in output.ranking:
        analysis = next(b for b in output.benefits if b.benefit_name == r.benefit_name)
        table.add_row(
            str(r.rank),
            r.benefit_name,
            f"{r.score:.2f}",
            label_styles.get(r.label.value, r.label.value),
            f"R${analysis.cac_estimate.blended_test_cac:,.2f}",
            f"R${analysis.acquisition_experiment.budget_recommended:,.2f}",
        )

    console.print(table)

    # Detalhe por benefício
    for analysis in output.benefits:
        console.print()
        console.print(
            Panel(
                f"[bold]{analysis.benefit_name.upper()}[/bold]",
                border_style="cyan",
            )
        )

        ct = analysis.search_demand.cluster_totals
        total = ct.awareness + ct.consideration + ct.action

        console.print(f"  Volume total: [bold]{total:,}[/bold]/mês")
        console.print(
            f"  Awareness: {ct.awareness:,} | "
            f"Consideration: {ct.consideration:,} | "
            f"Action: {ct.action:,}"
        )
        console.print(f"  Keywords analisadas: {len(analysis.search_demand.keywords)}")

        console.print()
        console.print(f"  [bold]Mercado endereçável:[/bold]")
        ms = analysis.market_size
        console.print(f"    Curiosos: {ms.curiosos:,}")
        console.print(f"    Explorando necessidade: {ms.explorando_necessidade:,}")
        console.print(f"    Agindo agora: {ms.agindo_agora:,}")
        console.print(
            f"    Total relevante: [bold]{ms.total_relevant_search_demand:,}[/bold]"
        )

        console.print()
        console.print(f"  [bold]CAC estimado:[/bold]")
        cac = analysis.cac_estimate
        console.print(f"    Awareness: R${cac.awareness:,.2f}")
        console.print(f"    Consideration: R${cac.consideration:,.2f}")
        console.print(f"    Action: R${cac.action:,.2f}")
        console.print(f"    Blended: [bold]R${cac.blended_test_cac:,.2f}[/bold]")

        console.print()
        diag = analysis.diagnosis
        console.print(f"  [bold]Diagnóstico:[/bold] {diag.label.value} (score: {diag.score})")
        for reason in diag.why:
            console.print(f"    • {reason}")

        console.print()
        console.print(f"  [bold]Persona:[/bold] {analysis.persona.persona_name}")
        console.print(f"    {analysis.persona.contexto_de_busca}")

        console.print()
        pitch = analysis.sales_pitch
        console.print(f"  [bold]Pitch:[/bold]")
        console.print(f"    Headline: {pitch.headline}")
        console.print(f"    Sub: {pitch.subheadline}")
        console.print(f"    CTA: {pitch.cta}")

        console.print()
        exp = analysis.acquisition_experiment
        console.print(f"  [bold]Experimento:[/bold]")
        console.print(f"    Orçamento: R${exp.budget_recommended:,.2f}")
        console.print(f"    Duração: {exp.duration_days} dias")
        console.print(f"    Grupos: {len(exp.campaign_structure)}")


@click.command()
@click.argument("input_files", nargs=-1, required=True, type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Salvar resultado em arquivo JSON",
)
@click.option("--json-only", is_flag=True, help="Apenas saída JSON, sem formatação")
def main(input_files: tuple[str, ...], output: str | None, json_only: bool) -> None:
    """Legal Demand Planner — Análise de demanda para benefícios e direitos.

    Recebe um ou mais arquivos JSON de input com configuração de benefícios.
    """
    try:
        inputs = _load_inputs(input_files)
    except Exception as e:
        console.print(f"[red]Erro ao carregar inputs: {e}[/red]")
        sys.exit(1)

    if not inputs:
        console.print("[red]Nenhum benefício encontrado nos arquivos de input.[/red]")
        sys.exit(1)

    if not json_only:
        console.print(f"Analisando {len(inputs)} benefício(s)...")

    result = run_pipeline(inputs)

    # JSON output
    result_json = result.model_dump(mode="json")

    if output:
        Path(output).write_text(json.dumps(result_json, indent=2, ensure_ascii=False))
        if not json_only:
            console.print(f"[green]Resultado salvo em {output}[/green]")

    if json_only:
        print(json.dumps(result_json, indent=2, ensure_ascii=False))
    else:
        _print_summary(result)


if __name__ == "__main__":
    main()
