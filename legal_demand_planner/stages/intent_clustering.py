"""Etapa 2 — Clusterização por estágio do funil.

Classifica cada keyword em Awareness, Consideration ou Action
usando regras semânticas e padrões lexicais.
"""

from __future__ import annotations

import re

from legal_demand_planner.models import ClusterTotals, IntentCluster, KeywordData

# Padrões ordenados por prioridade (Action > Consideration > Awareness)
# Action é checado primeiro porque é o cluster mais valioso

_ACTION_PATTERNS = [
    r"\bcomo solicitar\b",
    r"\bdar entrada\b",
    r"\bentrar com pedido\b",
    r"\badvogad[oa]\b",
    r"\bespecialista\b",
    r"\bconsulta\b",
    r"\bconsultar\b",
    r"\bajuda\b",
    r"\bfalar com\b",
    r"\bcontratar\b",
    r"\bpedir\b",
    r"\brecorrer\b",
    r"\brecurso\b",
    r"\bentrar na justiça\b",
    r"\bprocesso\b",
    r"\brequerimento\b",
    r"\bsolicitar\b",
    r"\bsolicitação\b",
    r"\bagendar\b",
    r"\bagendamento\b",
    r"\batendimento\b",
]

_CONSIDERATION_PATTERNS = [
    r"\bquem tem direito\b",
    r"\bdocumento[s]?\b",
    r"\bvalor\b",
    r"\brequisito[s]?\b",
    r"\bprazo\b",
    r"\bposso receber\b",
    r"\btenho direito\b",
    r"\brenda familiar\b",
    r"\brenda\b",
    r"\bidade\b",
    r"\bidoso\b",
    r"\bautista\b",
    r"\bdeficien\b",
    r"\bmei\b",
    r"\bautônom[oa]\b",
    r"\bdesempregad[oa]\b",
    r"\bclt\b",
    r"\bcontribuição\b",
    r"\bcontribuinte\b",
    r"\bcomo receber\b",
    r"\bquanto\b",
    r"\bcálculo\b",
    r"\bcalcular\b",
    r"\bsimulação\b",
    r"\bsimulador\b",
    r"\btabela\b",
    r"\bcritério[s]?\b",
    r"\belegib\b",
    r"\binss\b",
    r"\bcnis\b",
]

_AWARENESS_PATTERNS = [
    r"\bo que é\b",
    r"\bcomo funciona\b",
    r"\bsignificado\b",
    r"\bguia\b",
    r"\bentenda\b",
    r"\bexplicação\b",
    r"\bresumo\b",
    r"\btipos de\b",
    r"\bcompleto\b",
    r"\btudo sobre\b",
    r"\bo que\b",
]


def classify_keyword(keyword: str) -> IntentCluster:
    """Classifica uma keyword em um cluster de intenção."""
    text = keyword.lower()

    for pattern in _ACTION_PATTERNS:
        if re.search(pattern, text):
            return IntentCluster.ACTION

    for pattern in _CONSIDERATION_PATTERNS:
        if re.search(pattern, text):
            return IntentCluster.CONSIDERATION

    for pattern in _AWARENESS_PATTERNS:
        if re.search(pattern, text):
            return IntentCluster.AWARENESS

    # Fallback: keywords curtas e genéricas tendem a ser Awareness
    if len(text.split()) <= 2:
        return IntentCluster.AWARENESS

    # Default para Consideration (pessoa buscando algo mais específico)
    return IntentCluster.CONSIDERATION


def cluster_keywords(keywords: list[KeywordData]) -> list[KeywordData]:
    """Classifica todas as keywords e retorna a lista atualizada."""
    for kw in keywords:
        kw.intent_cluster = classify_keyword(kw.keyword)
    return keywords


def compute_cluster_totals(keywords: list[KeywordData]) -> ClusterTotals:
    """Soma o volume de buscas por cluster."""
    totals = ClusterTotals()
    for kw in keywords:
        volume = kw.avg_monthly_searches
        if kw.intent_cluster == IntentCluster.AWARENESS:
            totals.awareness += volume
        elif kw.intent_cluster == IntentCluster.CONSIDERATION:
            totals.consideration += volume
        elif kw.intent_cluster == IntentCluster.ACTION:
            totals.action += volume
    return totals
