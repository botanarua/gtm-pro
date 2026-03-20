"""Etapa 5 — Diagnóstico do potencial do mercado.

Classifica cada tema em: Testar, Testar com cautela, Não testar.
"""

from __future__ import annotations

from legal_demand_planner.config import (
    DEFAULT_DIAGNOSIS_THRESHOLDS,
    DEFAULT_DIAGNOSIS_WEIGHTS,
    DiagnosisThresholds,
    DiagnosisWeights,
)
from legal_demand_planner.models import (
    BenefitInput,
    CACEstimate,
    ClusterTotals,
    Diagnosis,
    DiagnosisLabel,
    KeywordData,
    MarketSize,
)


def _demand_score(market_size: MarketSize) -> float:
    """Score de 0 a 1 baseado no tamanho da demanda relevante."""
    total = market_size.total_relevant_search_demand
    if total >= 50000:
        return 1.0
    if total >= 20000:
        return 0.8
    if total >= 10000:
        return 0.6
    if total >= 5000:
        return 0.4
    if total >= 1000:
        return 0.2
    return 0.1


def _cac_score(cac_estimate: CACEstimate, target_cpa: float) -> float:
    """Score de 0 a 1 baseado na relação CAC estimado vs CAC alvo."""
    if cac_estimate.blended_test_cac <= 0:
        return 0.0
    ratio = target_cpa / cac_estimate.blended_test_cac
    if ratio >= 2.0:
        return 1.0
    if ratio >= 1.5:
        return 0.8
    if ratio >= 1.0:
        return 0.6
    if ratio >= 0.7:
        return 0.4
    if ratio >= 0.5:
        return 0.2
    return 0.1


def _action_consideration_score(cluster_totals: ClusterTotals) -> float:
    """Score de 0 a 1 baseado na proporção de Action + Consideration."""
    total = cluster_totals.awareness + cluster_totals.consideration + cluster_totals.action
    if total == 0:
        return 0.0
    ac_ratio = (cluster_totals.action + cluster_totals.consideration) / total
    return min(1.0, ac_ratio * 1.2)  # Leve boost


def _trend_score(keywords: list[KeywordData]) -> float:
    """Score de 0 a 1 baseado na tendência de crescimento YoY."""
    yoy_values = [kw.yoy_change for kw in keywords if kw.yoy_change is not None]
    if not yoy_values:
        return 0.5  # Neutro quando sem dados

    avg_yoy = sum(yoy_values) / len(yoy_values)
    if avg_yoy >= 0.20:
        return 1.0
    if avg_yoy >= 0.10:
        return 0.8
    if avg_yoy >= 0.0:
        return 0.6
    if avg_yoy >= -0.10:
        return 0.4
    return 0.2


def diagnose(
    keywords: list[KeywordData],
    cluster_totals: ClusterTotals,
    market_size: MarketSize,
    cac_estimate: CACEstimate,
    benefit_input: BenefitInput,
    weights: DiagnosisWeights | None = None,
    thresholds: DiagnosisThresholds | None = None,
) -> Diagnosis:
    """Gera o diagnóstico de viabilidade para um benefício."""
    if weights is None:
        weights = DEFAULT_DIAGNOSIS_WEIGHTS
    if thresholds is None:
        thresholds = DEFAULT_DIAGNOSIS_THRESHOLDS

    d_score = _demand_score(market_size)
    c_score = _cac_score(cac_estimate, benefit_input.target_cpa_threshold)
    ac_score = _action_consideration_score(cluster_totals)
    t_score = _trend_score(keywords)

    final_score = (
        d_score * weights.demand_size
        + c_score * weights.cac_estimate
        + ac_score * weights.action_consideration_ratio
        + t_score * weights.growth_trend
    )

    # Classificar
    if final_score >= thresholds.score_test:
        label = DiagnosisLabel.TEST
    elif final_score >= thresholds.score_test_cautious:
        label = DiagnosisLabel.TEST_CAUTIOUS
    else:
        label = DiagnosisLabel.DO_NOT_TEST

    # Justificativas
    why: list[str] = []
    total_volume = cluster_totals.awareness + cluster_totals.consideration + cluster_totals.action

    why.append(f"Volume total de buscas: {total_volume:,}/mês")
    why.append(
        f"Distribuição: Awareness {cluster_totals.awareness:,} | "
        f"Consideration {cluster_totals.consideration:,} | "
        f"Action {cluster_totals.action:,}"
    )
    why.append(f"CAC blended estimado: R${cac_estimate.blended_test_cac:,.2f}")
    why.append(f"CAC alvo: R${benefit_input.target_cpa_threshold:,.2f}")

    if cac_estimate.blended_test_cac > benefit_input.target_cpa_threshold:
        why.append("CAC estimado acima do limite — testar com cautela ou otimizar funil")
    else:
        why.append("CAC estimado dentro do aceitável")

    if ac_score < 0.4:
        why.append("Demanda concentrada em Awareness — maior foco em conteúdo que aquisição")
    elif ac_score > 0.7:
        why.append("Boa proporção de intenção prática (Consideration + Action)")

    why.append(f"Score final: {final_score:.2f}")

    return Diagnosis(
        label=label,
        score=round(final_score, 2),
        why=why,
    )
