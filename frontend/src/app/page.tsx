"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { BenefitInput } from "@/lib/types";
import { listBenefits, analyzeBenefit } from "@/lib/api";

export default function Home() {
  const router = useRouter();
  const [benefits, setBenefits] = useState<BenefitInput[]>([]);
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listBenefits().then(setBenefits).catch(() => setError("Não foi possível conectar à API"));
  }, []);

  async function handleAnalyze(benefit: BenefitInput) {
    setLoading(benefit.benefit_name);
    setError(null);
    try {
      const result = await analyzeBenefit(benefit);
      sessionStorage.setItem("analysis", JSON.stringify(result));
      sessionStorage.setItem("target_cpa", String(benefit.target_cpa_threshold));
      router.push("/analysis");
    } catch {
      setError("Falha na análise. Verifique se a API está rodando.");
      setLoading(null);
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="max-w-3xl w-full">
        <h1 className="text-3xl font-bold mb-2">Legal Demand Planner</h1>
        <p className="text-gray-500 mb-8">
          Escolha um benefício para analisar a demanda de busca e definir a jornada de aquisição.
        </p>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 mb-6 text-sm">
            {error}
          </div>
        )}

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {benefits.map((b) => (
            <div
              key={b.benefit_name}
              className="bg-white rounded-xl border border-gray-200 p-5 flex flex-col hover:border-indigo-300 hover:shadow-md transition-all"
            >
              <h2 className="font-semibold text-lg mb-2 capitalize">{b.benefit_name}</h2>
              <div className="flex flex-wrap gap-1 mb-4 flex-1">
                {b.seed_keywords.slice(0, 4).map((kw) => (
                  <span key={kw} className="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">
                    {kw}
                  </span>
                ))}
                {b.seed_keywords.length > 4 && (
                  <span className="text-gray-400 text-xs py-0.5">+{b.seed_keywords.length - 4}</span>
                )}
              </div>
              <button
                onClick={() => handleAnalyze(b)}
                disabled={loading !== null}
                className="w-full bg-indigo-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading === b.benefit_name ? (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    Analisando...
                  </span>
                ) : (
                  "Analisar"
                )}
              </button>
            </div>
          ))}
        </div>

        {benefits.length === 0 && !error && (
          <div className="text-center text-gray-400 py-12">Carregando benefícios...</div>
        )}
      </div>
    </div>
  );
}
