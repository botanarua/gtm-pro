"""CLI entry point for the Legal Demand Planner."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

from legal_demand_planner.models import BenefitAnalysis, BenefitInput
from legal_demand_planner.pipeline import analyze_benefit

console = Console()


def _print_analysis(analysis: BenefitAnalysis) -> None:
    """Imprime análise formatada no terminal."""
    console.print()
    console.print(
        Panel.fit(
            f"[bold]Legal Demand Planner — {analysis.benefit_name.upper()}[/bold]",
            border_style="blue",
        )
    )

    label_styles = {
        "testar": "[bold green]TESTAR[/bold green]",
        "testar_com_cautela": "[bold yellow]TESTAR COM CAUTELA[/bold yellow]",
        "nao_testar": "[bold red]NÃO TESTAR[/bold red]",
    }

    # Diagnóstico resumido no topo
    diag = analysis.diagnosis
    label_display = label_styles.get(diag.label.value, diag.label.value)
    console.print(f"\n  Diagnóstico: {label_display} (score: {diag.score})")

    # Demanda
    ct = analysis.search_demand.cluster_totals
    total = ct.awareness + ct.consideration + ct.action

    console.print(f"\n  [bold]Demanda de busca:[/bold]")
    console.print(f"    Volume total: [bold]{total:,}[/bold]/mês")
    console.print(
        f"    Awareness: {ct.awareness:,} | "
        f"Consideration: {ct.consideration:,} | "
        f"Action: {ct.action:,}"
    )
    console.print(f"    Keywords analisadas: {len(analysis.search_demand.keywords)}")

    # Mercado
    console.print(f"\n  [bold]Mercado endereçável:[/bold]")
    ms = analysis.market_size
    console.print(f"    Curiosos: {ms.curiosos:,}")
    console.print(f"    Explorando necessidade: {ms.explorando_necessidade:,}")
    console.print(f"    Agindo agora: {ms.agindo_agora:,}")
    console.print(
        f"    Total relevante: [bold]{ms.total_relevant_search_demand:,}[/bold]"
    )

    # CAC
    console.print(f"\n  [bold]CAC estimado:[/bold]")
    cac = analysis.cac_estimate
    console.print(f"    Awareness: R${cac.awareness:,.2f}")
    console.print(f"    Consideration: R${cac.consideration:,.2f}")
    console.print(f"    Action: R${cac.action:,.2f}")
    console.print(f"    Blended: [bold]R${cac.blended_test_cac:,.2f}[/bold]")

    # Justificativas do diagnóstico
    console.print(f"\n  [bold]Justificativa:[/bold]")
    for reason in diag.why:
        console.print(f"    • {reason}")

    # Persona
    console.print(f"\n  [bold]Persona:[/bold] {analysis.persona.persona_name}")
    console.print(f"    {analysis.persona.contexto_de_busca}")

    # Pitch
    console.print(f"\n  [bold]Pitch:[/bold]")
    pitch = analysis.sales_pitch
    console.print(f"    Headline: {pitch.headline}")
    console.print(f"    Sub: {pitch.subheadline}")
    console.print(f"    CTA: {pitch.cta}")
    console.print(f"    Por quê: {pitch.why_this_message}")
    for angle in pitch.angles:
        console.print(f"    • {angle}")

    # Experimento
    console.print(f"\n  [bold]Experimento de aquisição:[/bold]")
    exp = analysis.acquisition_experiment
    console.print(f"    Canal: Google Ads {exp.campaign_type.title()}")
    console.print(f"    Orçamento: R${exp.budget_recommended:,.2f}")
    console.print(f"    Duração: {exp.duration_days} dias")
    console.print(f"    Grupos de anúncio: {len(exp.campaign_structure)}")
    for group in exp.campaign_structure:
        console.print(f"\n    [{group.cluster.value.upper()}]")
        console.print(f"      Mensagem: {group.message}")
        console.print(f"      Keywords: {', '.join(group.keywords[:5])}")

    console.print()


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Salvar resultado em arquivo JSON",
)
@click.option("--json-only", is_flag=True, help="Apenas saída JSON, sem formatação")
def main(input_file: str, output: str | None, json_only: bool) -> None:
    """Legal Demand Planner — Análise de demanda para um benefício ou direito.

    Recebe um arquivo JSON com a configuração do benefício a analisar.
    """
    try:
        with open(input_file) as f:
            data = json.load(f)
        benefit_input = BenefitInput(**data)
    except Exception as e:
        console.print(f"[red]Erro ao carregar input: {e}[/red]")
        sys.exit(1)

    if not json_only:
        console.print(f"Analisando [bold]{benefit_input.benefit_name}[/bold]...")

    result = analyze_benefit(benefit_input)

    result_json = result.model_dump(mode="json")

    if output:
        Path(output).write_text(json.dumps(result_json, indent=2, ensure_ascii=False))
        if not json_only:
            console.print(f"[green]Resultado salvo em {output}[/green]")

    if json_only:
        print(json.dumps(result_json, indent=2, ensure_ascii=False))
    else:
        _print_analysis(result)


if __name__ == "__main__":
    main()
