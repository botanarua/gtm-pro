"""Etapa 7 — Geração de pitch de vendas.

Cria proposta de valor baseada em demanda, persona e cluster dominante.
"""

from __future__ import annotations

from legal_demand_planner.models import (
    BenefitInput,
    ClusterTotals,
    IntentCluster,
    Persona,
    SalesPitch,
)


def _dominant_cluster(cluster_totals: ClusterTotals) -> IntentCluster:
    clusters = {
        IntentCluster.AWARENESS: cluster_totals.awareness,
        IntentCluster.CONSIDERATION: cluster_totals.consideration,
        IntentCluster.ACTION: cluster_totals.action,
    }
    return max(clusters, key=clusters.get)  # type: ignore[arg-type]


def generate_pitch(
    cluster_totals: ClusterTotals,
    persona: Persona,
    benefit_input: BenefitInput,
) -> SalesPitch:
    """Gera o pitch de vendas baseado no cluster dominante."""
    benefit = benefit_input.benefit_name
    dominant = _dominant_cluster(cluster_totals)

    if dominant == IntentCluster.AWARENESS:
        return SalesPitch(
            core_promise=(
                f"Descubra se você tem direito ao {benefit} — "
                f"de forma simples, gratuita e sem compromisso."
            ),
            headline=f"Você pode ter direito ao {benefit} e não sabe",
            subheadline=(
                f"Milhares de brasileiros deixam de receber o {benefit} "
                f"por falta de informação. Descubra agora se você se encaixa."
            ),
            cta="Quero descobrir meu direito",
            why_this_message=(
                f"A maioria das buscas sobre {benefit} é de pessoas que ainda "
                f"estão descobrindo o tema. A mensagem foca em educação e "
                f"redução de barreira de entrada."
            ),
            angles=[
                f"Educativo: 'O que é o {benefit} e por que você pode ter direito'",
                f"Revelação: 'Milhares não sabem que podem receber o {benefit}'",
                f"Simplicidade: 'Entenda em 2 minutos se o {benefit} é pra você'",
            ],
        )

    if dominant == IntentCluster.CONSIDERATION:
        return SalesPitch(
            core_promise=(
                f"Descubra em minutos se você tem direito ao {benefit} "
                f"e quanto pode receber."
            ),
            headline=f"Será que você tem direito ao {benefit}?",
            subheadline=(
                f"Responda algumas perguntas simples e descubra se você "
                f"atende aos requisitos para receber o {benefit}."
            ),
            cta="Verificar meu direito agora",
            why_this_message=(
                f"As buscas mostram que o público está ativamente avaliando "
                f"se tem direito ao {benefit}. A mensagem foca em elegibilidade "
                f"e clareza sobre requisitos."
            ),
            angles=[
                f"Elegibilidade: 'Descubra se você atende aos requisitos do {benefit}'",
                f"Calculadora: 'Simule quanto você pode receber de {benefit}'",
                f"Checklist: 'Os documentos que você precisa para pedir o {benefit}'",
            ],
        )

    # Action dominant
    return SalesPitch(
        core_promise=(
            f"Receba orientação especializada para dar entrada no seu {benefit} "
            f"com segurança e agilidade."
        ),
        headline=f"Precisa de ajuda para solicitar o {benefit}?",
        subheadline=(
            f"Nossos especialistas ajudam você a dar entrada no {benefit} "
            f"sem burocracia e sem risco de negativa por erro."
        ),
        cta="Falar com especialista agora",
        why_this_message=(
            f"As buscas indicam que o público está pronto para agir e busca "
            f"ajuda prática. A mensagem foca em ação imediata e suporte "
            f"profissional."
        ),
        angles=[
            f"Urgência: 'Não perca o prazo — solicite o {benefit} hoje'",
            f"Segurança: 'Evite negativas — peça o {benefit} com orientação'",
            f"Facilidade: 'Dê entrada no {benefit} sem sair de casa'",
        ],
    )
