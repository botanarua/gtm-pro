"""Etapa 6 — Construção de persona com Jobs to Be Done.

Gera uma persona prática baseada nas buscas e intenções identificadas.
"""

from __future__ import annotations

from legal_demand_planner.models import (
    BenefitInput,
    ClusterTotals,
    IntentCluster,
    KeywordData,
    Persona,
)


def _top_keywords_by_cluster(
    keywords: list[KeywordData], cluster: IntentCluster, limit: int = 5
) -> list[str]:
    """Retorna as top keywords de um cluster ordenadas por volume."""
    cluster_kws = [kw for kw in keywords if kw.intent_cluster == cluster]
    cluster_kws.sort(key=lambda k: k.avg_monthly_searches, reverse=True)
    return [kw.keyword for kw in cluster_kws[:limit]]


def _dominant_cluster(cluster_totals: ClusterTotals) -> IntentCluster:
    """Identifica o cluster dominante por volume."""
    clusters = {
        IntentCluster.AWARENESS: cluster_totals.awareness,
        IntentCluster.CONSIDERATION: cluster_totals.consideration,
        IntentCluster.ACTION: cluster_totals.action,
    }
    return max(clusters, key=clusters.get)  # type: ignore[arg-type]


def build_persona(
    keywords: list[KeywordData],
    cluster_totals: ClusterTotals,
    benefit_input: BenefitInput,
) -> Persona:
    """Constrói a persona JTBD a partir dos dados de busca."""
    benefit = benefit_input.benefit_name
    dominant = _dominant_cluster(cluster_totals)

    top_awareness = _top_keywords_by_cluster(keywords, IntentCluster.AWARENESS)
    top_consideration = _top_keywords_by_cluster(keywords, IntentCluster.CONSIDERATION)
    top_action = _top_keywords_by_cluster(keywords, IntentCluster.ACTION)

    all_keywords = [kw.keyword for kw in sorted(
        keywords, key=lambda k: k.avg_monthly_searches, reverse=True
    )[:10]]

    # Contexto baseado no cluster dominante
    context_map = {
        IntentCluster.AWARENESS: (
            f"Pessoa que está descobrindo o {benefit} e quer entender se existe um "
            f"direito que se aplica à sua situação. Busca principalmente informações "
            f"gerais e educativas."
        ),
        IntentCluster.CONSIDERATION: (
            f"Pessoa que já sabe que o {benefit} existe e está tentando entender "
            f"se tem direito, quais documentos precisa e quanto pode receber. "
            f"Busca informações práticas sobre elegibilidade."
        ),
        IntentCluster.ACTION: (
            f"Pessoa que já sabe que precisa do {benefit} e está buscando como "
            f"dar entrada, encontrar ajuda profissional ou resolver seu caso. "
            f"Está pronta para agir."
        ),
    }

    # Persona name baseada no benefício
    persona_names = {
        IntentCluster.AWARENESS: f"Descobridor(a) do {benefit}",
        IntentCluster.CONSIDERATION: f"Avaliador(a) do {benefit}",
        IntentCluster.ACTION: f"Solicitante do {benefit}",
    }

    return Persona(
        persona_name=persona_names[dominant],
        contexto_de_busca=context_map[dominant],
        o_que_pesquisa=all_keywords,
        necessidades_urgentes=[
            f"Entender se tem direito ao {benefit}",
            f"Saber quais documentos precisa reunir",
            f"Descobrir o valor que pode receber",
            f"Saber como dar entrada no pedido",
        ],
        necessidades_latentes=[
            f"Segurança de que não vai perder o prazo",
            f"Confiança de que não vai ser negado por erro",
            f"Clareza sobre o processo sem linguagem jurídica",
            f"Saber se vale a pena buscar ajuda profissional",
        ],
        job_functional=[
            f"Acessar o {benefit} da forma mais rápida e segura possível",
            "Reunir a documentação correta sem idas desnecessárias",
            "Entender o passo a passo do processo",
        ],
        job_emotional=[
            "Sentir que tem controle sobre a própria situação",
            "Reduzir a ansiedade sobre o resultado do pedido",
            "Sentir que está sendo bem orientado(a)",
        ],
        job_social=[
            "Poder explicar para a família que está resolvendo",
            "Não depender de terceiros para informações básicas",
            "Sentir que está exercendo um direito legítimo",
        ],
        principais_objecoes=[
            "Não sei se realmente tenho direito",
            "Tenho medo de ser negado",
            "Não quero gastar dinheiro com advogado sem garantia",
            "O processo parece complicado demais",
            "Não sei em quem confiar",
        ],
        gatilhos_de_acao=[
            "Descobrir que tem direito e não sabia",
            "Ver que outras pessoas na mesma situação conseguiram",
            "Entender que o prazo está correndo",
            "Receber orientação clara e sem custo inicial",
            "Simulação de valor que pode receber",
        ],
        linguagem_usada_pelo_publico=(
            top_awareness[:3] + top_consideration[:3] + top_action[:3]
        ),
        principais_conteudos_ranqueados=[
            f"Guia completo sobre {benefit}",
            f"Quem tem direito ao {benefit}",
            f"Como solicitar {benefit} passo a passo",
            f"Documentos necessários para {benefit}",
            f"Valor do {benefit} atualizado",
        ],
    )
