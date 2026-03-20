"""Default configuration for the Legal Demand Planner."""

from pydantic import BaseModel


class ClusterUtilizationRates(BaseModel):
    """Taxas de aproveitamento por cluster de intenção."""

    awareness_low: float = 0.10
    awareness_high: float = 0.20
    consideration_low: float = 0.25
    consideration_high: float = 0.40
    action_low: float = 0.50
    action_high: float = 0.80


class DiagnosisWeights(BaseModel):
    """Pesos para o score de diagnóstico."""

    demand_size: float = 0.35
    cac_estimate: float = 0.35
    action_consideration_ratio: float = 0.20
    growth_trend: float = 0.10


class ExperimentDefaults(BaseModel):
    """Defaults para planejamento de experimento."""

    duration_days: int = 14
    target_clicks_per_cluster: int = 80
    num_clusters: int = 3


class DiagnosisThresholds(BaseModel):
    """Limiares para classificação do diagnóstico."""

    score_test: float = 0.65
    score_test_cautious: float = 0.40


DEFAULT_CLUSTER_RATES = ClusterUtilizationRates()
DEFAULT_DIAGNOSIS_WEIGHTS = DiagnosisWeights()
DEFAULT_EXPERIMENT = ExperimentDefaults()
DEFAULT_DIAGNOSIS_THRESHOLDS = DiagnosisThresholds()
