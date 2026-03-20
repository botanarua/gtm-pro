import { BenefitInput, BenefitAnalysis } from "./types";

const API_BASE = "http://localhost:8000";

export async function listBenefits(): Promise<BenefitInput[]> {
  const res = await fetch(`${API_BASE}/api/benefits`);
  if (!res.ok) throw new Error("Falha ao carregar benefícios");
  return res.json();
}

export async function analyzeBenefit(
  input: BenefitInput
): Promise<BenefitAnalysis> {
  const res = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!res.ok) throw new Error("Falha na análise");
  return res.json();
}
