export interface BenefitInput {
  benefit_name: string;
  country: string;
  language: string;
  seed_keywords: string[];
  conversion_rate_assumption: number;
  lead_to_client_rate_assumption: number;
  target_cpa_threshold: number;
  monthly_budget_test: number;
}

export interface KeywordData {
  keyword: string;
  avg_monthly_searches: number;
  competition: string;
  top_of_page_bid_low: number;
  top_of_page_bid_high: number;
  intent_cluster: "awareness" | "consideration" | "action" | null;
}

export interface ClusterTotals {
  awareness: number;
  consideration: number;
  action: number;
}

export interface SearchDemand {
  keywords: KeywordData[];
  cluster_totals: ClusterTotals;
}

export interface MarketSize {
  curiosos: number;
  explorando_necessidade: number;
  agindo_agora: number;
  total_relevant_search_demand: number;
}

export interface CACEstimate {
  awareness: number;
  consideration: number;
  action: number;
  blended_test_cac: number;
}

export interface Diagnosis {
  label: "testar" | "testar_com_cautela" | "nao_testar";
  score: number;
  why: string[];
}

export interface Persona {
  persona_name: string;
  contexto_de_busca: string;
  o_que_pesquisa: string[];
  necessidades_urgentes: string[];
  necessidades_latentes: string[];
  job_functional: string[];
  job_emotional: string[];
  job_social: string[];
  principais_objecoes: string[];
  gatilhos_de_acao: string[];
  linguagem_usada_pelo_publico: string[];
  principais_conteudos_ranqueados: string[];
}

export interface SalesPitch {
  core_promise: string;
  headline: string;
  subheadline: string;
  cta: string;
  why_this_message: string;
  angles: string[];
}

export interface AdGroupPlan {
  cluster: "awareness" | "consideration" | "action";
  keywords: string[];
  message: string;
  responsive_ad_headlines: string[];
  responsive_ad_descriptions: string[];
}

export interface AcquisitionExperiment {
  campaign_type: string;
  duration_days: number;
  budget_recommended: number;
  campaign_structure: AdGroupPlan[];
  success_metrics: string[];
}

export interface BenefitAnalysis {
  benefit_name: string;
  search_demand: SearchDemand;
  market_size: MarketSize;
  cac_estimate: CACEstimate;
  diagnosis: Diagnosis;
  persona: Persona;
  sales_pitch: SalesPitch;
  acquisition_experiment: AcquisitionExperiment;
}
