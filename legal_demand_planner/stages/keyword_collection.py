"""Etapa 1 — Identificação de demanda via Google Search.

No MVP, aceita dados pré-coletados do Google Ads Keyword Planner ou
gera dados simulados a partir das seed keywords para demonstração.
Em produção, integraria com a API do Google Ads Keyword Planner.
"""

from __future__ import annotations

import hashlib
import re

from legal_demand_planner.models import BenefitInput, KeywordData


# Variações comuns de busca para benefícios jurídicos brasileiros
_EXPANSION_TEMPLATES = [
    "{seed}",
    "o que é {seed}",
    "como funciona {seed}",
    "{seed} quem tem direito",
    "{seed} documentos",
    "{seed} valor",
    "{seed} como solicitar",
    "{seed} requisitos",
    "{seed} prazo",
    "{seed} advogado",
    "{seed} dar entrada",
    "{seed} inss",
    "{seed} consulta",
    "{seed} especialista",
    "{seed} ajuda",
    "{seed} mei",
    "{seed} autônomo",
    "{seed} desempregado",
    "{seed} idoso",
    "{seed} posso receber",
    "{seed} entrar com pedido",
    "{seed} guia completo",
    "{seed} significado",
]

# Termos irrelevantes que devem ser filtrados
_IRRELEVANT_PATTERNS = [
    r"\bemprego\b",
    r"\bconcurso\b",
    r"\bvestibular\b",
    r"\bfaculdade\b",
    r"\bcurso\b",
    r"\bjogo\b",
    r"\bfutebol\b",
    r"\bnovela\b",
    r"\bfofoca\b",
    r"\breceita de\b",
]


def _normalize(keyword: str) -> str:
    """Normaliza keyword para comparação."""
    text = keyword.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def _is_irrelevant(keyword: str) -> bool:
    for pattern in _IRRELEVANT_PATTERNS:
        if re.search(pattern, keyword, re.IGNORECASE):
            return True
    return False


def _deterministic_volume(keyword: str, base: int = 1000) -> int:
    """Gera volume determinístico baseado no hash da keyword (para demo)."""
    h = int(hashlib.md5(keyword.encode()).hexdigest()[:8], 16)
    return max(10, (h % base) * 10)


def _deterministic_bid(keyword: str) -> tuple[float, float]:
    """Gera bids determinísticos baseados no hash da keyword (para demo)."""
    h = int(hashlib.md5(keyword.encode()).hexdigest()[8:16], 16)
    low = round(0.50 + (h % 400) / 100, 2)
    high = round(low + 0.50 + (h % 300) / 100, 2)
    return low, high


def expand_keywords(benefit_input: BenefitInput) -> list[KeywordData]:
    """Expande seed keywords em lista completa com dados simulados.

    Em produção, substituir por chamada à API do Google Ads Keyword Planner.
    """
    seen: set[str] = set()
    keywords: list[KeywordData] = []

    for seed in benefit_input.seed_keywords:
        for template in _EXPANSION_TEMPLATES:
            kw = template.format(seed=seed)
            normalized = _normalize(kw)

            if normalized in seen:
                continue
            if _is_irrelevant(normalized):
                continue

            seen.add(normalized)
            volume = _deterministic_volume(normalized)
            bid_low, bid_high = _deterministic_bid(normalized)

            competitions = ["LOW", "MEDIUM", "HIGH"]
            comp_idx = int(hashlib.md5(normalized.encode()).hexdigest()[0], 16) % 3

            keywords.append(
                KeywordData(
                    keyword=normalized,
                    avg_monthly_searches=volume,
                    competition=competitions[comp_idx],
                    top_of_page_bid_low=bid_low,
                    top_of_page_bid_high=bid_high,
                    three_month_change=None,
                    yoy_change=None,
                    source_seed=seed,
                )
            )

    return keywords


def load_keywords_from_data(
    raw_keywords: list[dict],
) -> list[KeywordData]:
    """Carrega keywords a partir de dados pré-coletados (ex: CSV do Keyword Planner)."""
    keywords = []
    seen: set[str] = set()

    for raw in raw_keywords:
        normalized = _normalize(raw.get("keyword", ""))
        if normalized in seen or _is_irrelevant(normalized):
            continue
        seen.add(normalized)
        keywords.append(KeywordData(**raw))

    return keywords
