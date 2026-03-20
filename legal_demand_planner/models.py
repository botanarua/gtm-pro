"""Pydantic models for Legal Demand Planner input and output."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# --- Enums ---


class IntentCluster(str, Enum):
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    ACTION = "action"


class DiagnosisLabel(str, Enum):
    TEST = "testar"
    TEST_CAUTIOUS = "testar_com_cautela"
    DO_NOT_TEST = "nao_testar"


# --- Input Models ---


class BenefitInput(BaseModel):
    """Entrada do sistema para um benefício/direito."""

    benefit_name: str
    country: str = "BR"
    language: str = "pt-BR"
    seed_keywords: list[str]
    conversion_rate_assumption: float = Field(
        default=0.08, description="Taxa de conversão estimada da landing page"
    )
    lead_to_client_rate_assumption: float = Field(
        default=0.20, description="Taxa estimada de lead para cliente"
    )
    target_cpa_threshold: float = Field(
        default=250.0, description="CAC alvo máximo em reais"
    )
    monthly_budget_test: float = Field(
        default=5000.0, description="Orçamento mensal de teste em reais"
    )


# --- Keyword Models ---


class KeywordData(BaseModel):
    """Dados de uma keyword coletada."""

    keyword: str
    avg_monthly_searches: int = 0
    competition: str = "LOW"
    top_of_page_bid_low: float = 0.0
    top_of_page_bid_high: float = 0.0
    three_month_change: Optional[float] = None
    yoy_change: Optional[float] = None
    source_seed: str = ""
    intent_cluster: Optional[IntentCluster] = None


# --- Output Models ---


class ClusterTotals(BaseModel):
    awareness: int = 0
    consideration: int = 0
    action: int = 0


class SearchDemand(BaseModel):
    keywords: list[KeywordData] = []
    cluster_totals: ClusterTotals = ClusterTotals()


class MarketSize(BaseModel):
    curiosos: int = 0
    explorando_necessidade: int = 0
    agindo_agora: int = 0
    total_relevant_search_demand: int = 0


class CACEstimate(BaseModel):
    awareness: float = 0.0
    consideration: float = 0.0
    action: float = 0.0
    blended_test_cac: float = 0.0


class Diagnosis(BaseModel):
    label: DiagnosisLabel = DiagnosisLabel.DO_NOT_TEST
    score: float = 0.0
    why: list[str] = []


class Persona(BaseModel):
    persona_name: str = ""
    contexto_de_busca: str = ""
    o_que_pesquisa: list[str] = []
    necessidades_urgentes: list[str] = []
    necessidades_latentes: list[str] = []
    job_functional: list[str] = []
    job_emotional: list[str] = []
    job_social: list[str] = []
    principais_objecoes: list[str] = []
    gatilhos_de_acao: list[str] = []
    linguagem_usada_pelo_publico: list[str] = []
    principais_conteudos_ranqueados: list[str] = []


class SalesPitch(BaseModel):
    core_promise: str = ""
    headline: str = ""
    subheadline: str = ""
    cta: str = ""
    why_this_message: str = ""
    angles: list[str] = []


class AdGroupPlan(BaseModel):
    cluster: IntentCluster
    keywords: list[str] = []
    message: str = ""
    responsive_ad_headlines: list[str] = []
    responsive_ad_descriptions: list[str] = []


class AcquisitionExperiment(BaseModel):
    campaign_type: str = "search"
    duration_days: int = 14
    budget_recommended: float = 0.0
    campaign_structure: list[AdGroupPlan] = []
    success_metrics: list[str] = [
        "impressões",
        "CTR",
        "CPC",
        "taxa de conversão",
        "CPL",
        "CAC estimado vs real",
        "termos reais acionados",
        "desempenho por cluster",
    ]


class BenefitAnalysis(BaseModel):
    """Saída completa da análise de um benefício."""

    benefit_name: str
    search_demand: SearchDemand = SearchDemand()
    market_size: MarketSize = MarketSize()
    cac_estimate: CACEstimate = CACEstimate()
    diagnosis: Diagnosis = Diagnosis()
    persona: Persona = Persona()
    sales_pitch: SalesPitch = SalesPitch()
    acquisition_experiment: AcquisitionExperiment = AcquisitionExperiment()


