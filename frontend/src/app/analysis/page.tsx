"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { BenefitAnalysis } from "@/lib/types";
import DiagnosisBadge from "@/components/DiagnosisBadge";
import DemandChart from "@/components/DemandChart";
import MarketFunnel from "@/components/MarketFunnel";
import CACComparison from "@/components/CACComparison";
import PersonaCard from "@/components/PersonaCard";
import PitchCard from "@/components/PitchCard";
import ExperimentPlan from "@/components/ExperimentPlan";

export default function AnalysisPage() {
  const router = useRouter();
  const [analysis, setAnalysis] = useState<BenefitAnalysis | null>(null);
  const [targetCpa, setTargetCpa] = useState(250);

  useEffect(() => {
    const stored = sessionStorage.getItem("analysis");
    const storedTarget = sessionStorage.getItem("target_cpa");
    if (!stored) {
      router.push("/");
      return;
    }
    setAnalysis(JSON.parse(stored));
    if (storedTarget) setTargetCpa(Number(storedTarget));
  }, [router]);

  if (!analysis) {
    return <div className="min-h-screen flex items-center justify-center text-gray-400">Carregando...</div>;
  }

  return (
    <div className="min-h-screen p-6 md:p-10">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center gap-4 mb-8">
          <button
            onClick={() => router.push("/")}
            className="text-gray-500 hover:text-gray-700 text-sm self-start"
          >
            &larr; Voltar
          </button>
          <div className="flex-1">
            <h1 className="text-2xl font-bold capitalize">{analysis.benefit_name}</h1>
          </div>
          <DiagnosisBadge label={analysis.diagnosis.label} score={analysis.diagnosis.score} />
        </div>

        {/* Justificativas do diagnóstico */}
        <div className="bg-white rounded-xl border border-gray-200 p-5 mb-6">
          <h3 className="font-semibold mb-2">Diagnóstico</h3>
          <ul className="space-y-1">
            {analysis.diagnosis.why.map((reason, i) => (
              <li key={i} className="text-sm text-gray-600 flex items-start gap-2">
                <span className="text-gray-400 mt-0.5">&#8226;</span>
                {reason}
              </li>
            ))}
          </ul>
        </div>

        {/* Grid principal */}
        <div className="grid gap-6 md:grid-cols-2">
          <DemandChart data={analysis.search_demand} />
          <MarketFunnel data={analysis.market_size} />
          <CACComparison data={analysis.cac_estimate} target={targetCpa} />
          <PersonaCard data={analysis.persona} />
          <PitchCard data={analysis.sales_pitch} />
          <ExperimentPlan data={analysis.acquisition_experiment} />
        </div>
      </div>
    </div>
  );
}
