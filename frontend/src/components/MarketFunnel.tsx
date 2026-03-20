"use client";

import { MarketSize } from "@/lib/types";

export default function MarketFunnel({ data }: { data: MarketSize }) {
  const max = Math.max(data.curiosos, data.explorando_necessidade, data.agindo_agora, 1);

  const stages = [
    { label: "Curiosos", value: data.curiosos, color: "bg-blue-300" },
    { label: "Explorando necessidade", value: data.explorando_necessidade, color: "bg-yellow-400" },
    { label: "Agindo agora", value: data.agindo_agora, color: "bg-green-400" },
  ];

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <h3 className="font-semibold text-lg mb-1">Mercado endereçável</h3>
      <p className="text-3xl font-bold text-gray-900 mb-4">
        {data.total_relevant_search_demand.toLocaleString("pt-BR")}
        <span className="text-base font-normal text-gray-500"> relevante/mês</span>
      </p>
      <div className="space-y-3">
        {stages.map((s) => (
          <div key={s.label}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600">{s.label}</span>
              <span className="font-medium">{s.value.toLocaleString("pt-BR")}</span>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-3">
              <div
                className={`${s.color} h-3 rounded-full transition-all`}
                style={{ width: `${(s.value / max) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
