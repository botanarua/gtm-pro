"""Etapa 9 — Ranking entre benefícios.

Compara múltiplos temas e prioriza os próximos testes.
"""

from __future__ import annotations

from legal_demand_planner.models import BenefitAnalysis, RankedBenefit


def rank_benefits(analyses: list[BenefitAnalysis]) -> list[RankedBenefit]:
    """Gera o ranking comparativo entre benefícios."""
    ranked: list[RankedBenefit] = []

    for analysis in analyses:
        observations: list[str] = []
        diag = analysis.diagnosis
        ct = analysis.search_demand.cluster_totals
        total_volume = ct.awareness + ct.consideration + ct.action

        observations.append(f"Score: {diag.score:.2f} — {diag.label.value}")
        observations.append(f"Volume total: {total_volume:,}/mês")

        if total_volume > 0:
            action_pct = ct.action / total_volume * 100
            consideration_pct = ct.consideration / total_volume * 100
            observations.append(
                f"Action: {action_pct:.0f}% | Consideration: {consideration_pct:.0f}%"
            )

        observations.append(
            f"CAC blended: R${analysis.cac_estimate.blended_test_cac:,.2f}"
        )
        observations.append(
            f"Orçamento recomendado: R${analysis.acquisition_experiment.budget_recommended:,.2f}"
        )

        ranked.append(
            RankedBenefit(
                rank=0,  # Will be set after sorting
                benefit_name=analysis.benefit_name,
                score=diag.score,
                label=diag.label,
                observations=observations,
            )
        )

    # Ordenar por score decrescente
    ranked.sort(key=lambda r: r.score, reverse=True)
    for i, item in enumerate(ranked):
        item.rank = i + 1

    return ranked
