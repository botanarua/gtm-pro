"""FastAPI backend for Legal Demand Planner."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from legal_demand_planner.models import BenefitAnalysis, BenefitInput
from legal_demand_planner.pipeline import analyze_benefit

app = FastAPI(title="Legal Demand Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


@app.get("/api/benefits")
def list_benefits() -> list[dict]:
    """Lista benefícios de exemplo disponíveis."""
    benefits = []
    for path in sorted(EXAMPLES_DIR.glob("*.json")):
        with open(path) as f:
            data = json.load(f)
        benefits.append(data)
    return benefits


@app.post("/api/analyze", response_model=BenefitAnalysis)
def run_analysis(benefit_input: BenefitInput) -> BenefitAnalysis:
    """Executa o pipeline completo para um benefício."""
    try:
        return analyze_benefit(benefit_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
