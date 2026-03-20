"""Etapa 8 — Planejamento do experimento de aquisição.

Sugere um primeiro teste de mídia no Google Ads Search.
"""

from __future__ import annotations

from legal_demand_planner.config import DEFAULT_EXPERIMENT, ExperimentDefaults
from legal_demand_planner.models import (
    AcquisitionExperiment,
    AdGroupPlan,
    BenefitInput,
    IntentCluster,
    KeywordData,
    SalesPitch,
)


def _avg_cpc(keywords: list[KeywordData], cluster: IntentCluster) -> float:
    cluster_kws = [kw for kw in keywords if kw.intent_cluster == cluster]
    if not cluster_kws:
        return 0.0
    return sum(
        (kw.top_of_page_bid_low + kw.top_of_page_bid_high) / 2 for kw in cluster_kws
    ) / len(cluster_kws)


def _top_keywords(
    keywords: list[KeywordData], cluster: IntentCluster, limit: int = 10
) -> list[str]:
    cluster_kws = [kw for kw in keywords if kw.intent_cluster == cluster]
    cluster_kws.sort(key=lambda k: k.avg_monthly_searches, reverse=True)
    return [kw.keyword for kw in cluster_kws[:limit]]


def plan_experiment(
    keywords: list[KeywordData],
    sales_pitch: SalesPitch,
    benefit_input: BenefitInput,
    defaults: ExperimentDefaults | None = None,
) -> AcquisitionExperiment:
    """Planeja o experimento de aquisição no Google Ads."""
    if defaults is None:
        defaults = DEFAULT_EXPERIMENT

    benefit = benefit_input.benefit_name

    # Calcular orçamento
    cpcs = {
        IntentCluster.AWARENESS: _avg_cpc(keywords, IntentCluster.AWARENESS),
        IntentCluster.CONSIDERATION: _avg_cpc(keywords, IntentCluster.CONSIDERATION),
        IntentCluster.ACTION: _avg_cpc(keywords, IntentCluster.ACTION),
    }

    overall_avg_cpc = sum(cpcs.values()) / max(len([v for v in cpcs.values() if v > 0]), 1)
    budget = defaults.target_clicks_per_cluster * overall_avg_cpc * defaults.num_clusters
    budget = max(budget, 300.0)  # Mínimo de R$300

    # Cap no orçamento mensal do teste
    budget = min(budget, benefit_input.monthly_budget_test)

    # Estrutura de campanha por cluster
    ad_groups = []

    # Awareness group
    awareness_kws = _top_keywords(keywords, IntentCluster.AWARENESS)
    if awareness_kws:
        ad_groups.append(
            AdGroupPlan(
                cluster=IntentCluster.AWARENESS,
                keywords=awareness_kws,
                message=f"Descubra o que é o {benefit} e se você tem direito",
                responsive_ad_headlines=[
                    f"O Que é {benefit.title()}?",
                    f"Descubra Seu Direito ao {benefit.title()}",
                    f"Guia Completo: {benefit.title()}",
                    f"Entenda o {benefit.title()} Agora",
                    f"Você Pode Ter Direito",
                ],
                responsive_ad_descriptions=[
                    f"Saiba tudo sobre {benefit} e descubra se você tem direito. Informação gratuita e sem compromisso.",
                    f"Milhares de brasileiros não sabem que têm direito ao {benefit}. Descubra agora.",
                ],
            )
        )

    # Consideration group
    consideration_kws = _top_keywords(keywords, IntentCluster.CONSIDERATION)
    if consideration_kws:
        ad_groups.append(
            AdGroupPlan(
                cluster=IntentCluster.CONSIDERATION,
                keywords=consideration_kws,
                message=f"Verifique se você atende aos requisitos do {benefit}",
                responsive_ad_headlines=[
                    f"Quem Tem Direito ao {benefit.title()}?",
                    f"Verifique Seus Requisitos",
                    f"Simule Seu {benefit.title()}",
                    f"Documentos Para {benefit.title()}",
                    f"Descubra Quanto Receber",
                ],
                responsive_ad_descriptions=[
                    f"Verifique em minutos se você tem direito ao {benefit}. Tire suas dúvidas sobre requisitos e documentos.",
                    f"Descubra se você atende aos critérios do {benefit} e quanto pode receber.",
                ],
            )
        )

    # Action group
    action_kws = _top_keywords(keywords, IntentCluster.ACTION)
    if action_kws:
        ad_groups.append(
            AdGroupPlan(
                cluster=IntentCluster.ACTION,
                keywords=action_kws,
                message=f"Dê entrada no {benefit} com ajuda especializada",
                responsive_ad_headlines=[
                    f"Solicitar {benefit.title()} Agora",
                    f"Especialista em {benefit.title()}",
                    f"Dar Entrada no {benefit.title()}",
                    f"Ajuda Com {benefit.title()}",
                    f"Atendimento Imediato",
                ],
                responsive_ad_descriptions=[
                    f"Precisa dar entrada no {benefit}? Nossos especialistas te ajudam sem burocracia. Atendimento imediato.",
                    f"Solicite o {benefit} com orientação profissional. Evite negativas e agilize seu pedido.",
                ],
            )
        )

    return AcquisitionExperiment(
        campaign_type="search",
        duration_days=defaults.duration_days,
        budget_recommended=round(budget, 2),
        campaign_structure=ad_groups,
        success_metrics=[
            "impressões",
            "CTR",
            "CPC real vs estimado",
            "taxa de conversão da landing page",
            "CPL (custo por lead)",
            "CAC estimado vs real",
            "termos de busca reais acionados",
            "desempenho por cluster (Awareness / Consideration / Action)",
        ],
    )
