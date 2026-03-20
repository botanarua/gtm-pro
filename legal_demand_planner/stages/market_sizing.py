"""Etapa 3 — Tamanho do mercado endereçável.

Traduz volume de busca em mercado potencial por estágio.
"""

from __future__ import annotations

from legal_demand_planner.config import DEFAULT_CLUSTER_RATES, ClusterUtilizationRates
from legal_demand_planner.models import ClusterTotals, MarketSize


def estimate_market_size(
    cluster_totals: ClusterTotals,
    rates: ClusterUtilizationRates | None = None,
) -> MarketSize:
    """Estima o tamanho do mercado endereçável por bucket.

    Usa o ponto médio das faixas de aproveitamento para cada cluster.
    """
    if rates is None:
        rates = DEFAULT_CLUSTER_RATES

    awareness_rate = (rates.awareness_low + rates.awareness_high) / 2
    consideration_rate = (rates.consideration_low + rates.consideration_high) / 2
    action_rate = (rates.action_low + rates.action_high) / 2

    curiosos = int(cluster_totals.awareness * awareness_rate)
    explorando = int(cluster_totals.consideration * consideration_rate)
    agindo = int(cluster_totals.action * action_rate)

    return MarketSize(
        curiosos=curiosos,
        explorando_necessidade=explorando,
        agindo_agora=agindo,
        total_relevant_search_demand=curiosos + explorando + agindo,
    )
