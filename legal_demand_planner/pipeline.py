"""Pipeline principal do Legal Demand Planner.

Orquestra todas as etapas de análise para um benefício.
"""

from __future__ import annotations

from legal_demand_planner.models import (
    BenefitAnalysis,
    BenefitInput,
    SearchDemand,
)
from legal_demand_planner.stages.cac_estimation import estimate_cac
from legal_demand_planner.stages.diagnosis import diagnose
from legal_demand_planner.stages.experiment_planner import plan_experiment
from legal_demand_planner.stages.intent_clustering import (
    cluster_keywords,
    compute_cluster_totals,
)
from legal_demand_planner.stages.keyword_collection import expand_keywords
from legal_demand_planner.stages.market_sizing import estimate_market_size
from legal_demand_planner.stages.persona_builder import build_persona
from legal_demand_planner.stages.pitch_generator import generate_pitch


def analyze_benefit(benefit_input: BenefitInput) -> BenefitAnalysis:
    """Executa o pipeline completo para um único benefício."""

    # Etapa 1 — Coleta/expansão de keywords
    keywords = expand_keywords(benefit_input)

    # Etapa 2 — Clusterização por intenção
    keywords = cluster_keywords(keywords)
    cluster_totals = compute_cluster_totals(keywords)

    # Etapa 3 — Tamanho do mercado
    market_size = estimate_market_size(cluster_totals)

    # Etapa 4 — Estimativa de CAC
    cac = estimate_cac(keywords, benefit_input)

    # Etapa 5 — Diagnóstico
    diag = diagnose(
        keywords=keywords,
        cluster_totals=cluster_totals,
        market_size=market_size,
        cac_estimate=cac,
        benefit_input=benefit_input,
    )

    # Etapa 6 — Persona JTBD
    persona = build_persona(keywords, cluster_totals, benefit_input)

    # Etapa 7 — Pitch de vendas
    pitch = generate_pitch(cluster_totals, persona, benefit_input)

    # Etapa 8 — Plano de experimento
    experiment = plan_experiment(keywords, pitch, benefit_input)

    return BenefitAnalysis(
        benefit_name=benefit_input.benefit_name,
        search_demand=SearchDemand(keywords=keywords, cluster_totals=cluster_totals),
        market_size=market_size,
        cac_estimate=cac,
        diagnosis=diag,
        persona=persona,
        sales_pitch=pitch,
        acquisition_experiment=experiment,
    )
