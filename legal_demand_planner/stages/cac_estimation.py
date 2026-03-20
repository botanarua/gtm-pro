"""Etapa 4 — Estimativa de CAC.

Estima o custo de aquisição por cluster com base em CPC e taxas assumidas.
"""

from __future__ import annotations

from legal_demand_planner.models import (
    BenefitInput,
    CACEstimate,
    IntentCluster,
    KeywordData,
)


def _avg_cpc_for_cluster(
    keywords: list[KeywordData], cluster: IntentCluster
) -> float:
    """Calcula CPC médio para um cluster."""
    cluster_kws = [kw for kw in keywords if kw.intent_cluster == cluster]
    if not cluster_kws:
        return 0.0
    total_cpc = sum(
        (kw.top_of_page_bid_low + kw.top_of_page_bid_high) / 2 for kw in cluster_kws
    )
    return total_cpc / len(cluster_kws)


def _estimate_cac_for_cpc(
    avg_cpc: float,
    conversion_rate: float,
    lead_to_client_rate: float,
) -> float:
    """Calcula CAC estimado a partir de CPC médio.

    cpc_mid / conversion_rate = CPL
    CPL / lead_to_client_rate = CAC
    """
    if conversion_rate <= 0 or lead_to_client_rate <= 0:
        return float("inf")
    cpl = avg_cpc / conversion_rate
    return cpl / lead_to_client_rate


def estimate_cac(
    keywords: list[KeywordData],
    benefit_input: BenefitInput,
) -> CACEstimate:
    """Estima CAC por cluster e blended."""
    cr = benefit_input.conversion_rate_assumption
    ltr = benefit_input.lead_to_client_rate_assumption

    cpc_awareness = _avg_cpc_for_cluster(keywords, IntentCluster.AWARENESS)
    cpc_consideration = _avg_cpc_for_cluster(keywords, IntentCluster.CONSIDERATION)
    cpc_action = _avg_cpc_for_cluster(keywords, IntentCluster.ACTION)

    cac_awareness = _estimate_cac_for_cpc(cpc_awareness, cr, ltr)
    cac_consideration = _estimate_cac_for_cpc(cpc_consideration, cr, ltr)
    cac_action = _estimate_cac_for_cpc(cpc_action, cr, ltr)

    # Blended CAC: peso maior em Action (50%) e Consideration (35%), Awareness (15%)
    weights = {
        IntentCluster.ACTION: 0.50,
        IntentCluster.CONSIDERATION: 0.35,
        IntentCluster.AWARENESS: 0.15,
    }
    cac_values = {
        IntentCluster.ACTION: cac_action,
        IntentCluster.CONSIDERATION: cac_consideration,
        IntentCluster.AWARENESS: cac_awareness,
    }

    # Só considera clusters com keywords válidas
    total_weight = 0.0
    blended = 0.0
    for cluster, weight in weights.items():
        cac = cac_values[cluster]
        if cac > 0 and cac != float("inf"):
            blended += cac * weight
            total_weight += weight

    blended_cac = blended / total_weight if total_weight > 0 else 0.0

    return CACEstimate(
        awareness=round(cac_awareness, 2),
        consideration=round(cac_consideration, 2),
        action=round(cac_action, 2),
        blended_test_cac=round(blended_cac, 2),
    )
