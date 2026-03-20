# Legal Demand Planner

Plataforma que transforma sinais de busca sobre benefícios e direitos do cidadão em decisão de lançamento, persona, pitch e plano de teste de aquisição para o NossoDireito.com e escritórios parceiros.

## Instalação

```bash
pip install -e .
```

## Uso

### Analisar um benefício

```bash
ldp examples/salario_maternidade.json
```

### Comparar múltiplos benefícios

```bash
ldp examples/bpc.json examples/salario_maternidade.json examples/aposentadoria.json
```

### Exportar resultado em JSON

```bash
ldp examples/bpc.json examples/salario_maternidade.json -o resultado.json
```

### Apenas JSON (sem formatação)

```bash
ldp examples/bpc.json --json-only
```

## Estrutura do Pipeline

1. **Coleta de keywords** — Expande seed keywords (simulado no MVP, integrável com Google Ads Keyword Planner)
2. **Clusterização por intenção** — Classifica buscas em Awareness, Consideration e Action
3. **Tamanho do mercado** — Estima mercado endereçável por estágio
4. **Estimativa de CAC** — Calcula CAC por cluster e blended
5. **Diagnóstico** — Classifica em Testar / Testar com cautela / Não testar
6. **Persona JTBD** — Gera persona baseada em buscas reais
7. **Pitch de vendas** — Cria proposta de valor alinhada ao cluster dominante
8. **Experimento de aquisição** — Planeja teste de Google Ads Search
9. **Ranking** — Compara e prioriza benefícios candidatos

## Input

Arquivo JSON por benefício:

```json
{
  "benefit_name": "salário-maternidade",
  "country": "BR",
  "language": "pt-BR",
  "seed_keywords": [
    "salário maternidade",
    "quem tem direito ao salário maternidade"
  ],
  "conversion_rate_assumption": 0.08,
  "lead_to_client_rate_assumption": 0.2,
  "target_cpa_threshold": 250,
  "monthly_budget_test": 5000
}
```

## Próximos passos

- Integração com Google Ads Keyword Planner API para dados reais
- Interface web para input e visualização
- Integração com LLM para classificação de intenção em casos ambíguos
- Dados históricos de tendência (3-month change, YoY change)
