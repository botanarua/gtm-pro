"use client";

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from "recharts";
import { CACEstimate } from "@/lib/types";

export default function CACComparison({ data, target }: { data: CACEstimate; target: number }) {
  const chartData = [
    { name: "Awareness", value: data.awareness, color: "#93c5fd" },
    { name: "Consideration", value: data.consideration, color: "#fbbf24" },
    { name: "Action", value: data.action, color: "#34d399" },
    { name: "Blended", value: data.blended_test_cac, color: "#8b5cf6" },
  ];

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <h3 className="font-semibold text-lg mb-1">CAC estimado</h3>
      <div className="flex items-baseline gap-3 mb-4">
        <p className="text-3xl font-bold">R${data.blended_test_cac.toFixed(0)}</p>
        <p className="text-sm text-gray-500">blended</p>
        <span className="text-sm text-gray-400">|</span>
        <p className="text-sm text-gray-500">Alvo: R${target.toFixed(0)}</p>
      </div>
      <ResponsiveContainer width="100%" height={180}>
        <BarChart data={chartData} margin={{ left: 10 }}>
          <XAxis dataKey="name" fontSize={12} />
          <YAxis tickFormatter={(v) => `R$${v}`} fontSize={12} />
          <Tooltip formatter={(v: number) => `R$${v.toFixed(2)}`} />
          <ReferenceLine y={target} stroke="#ef4444" strokeDasharray="6 3" label={{ value: "Alvo", fill: "#ef4444", fontSize: 11 }} />
          <Bar dataKey="value" radius={[6, 6, 0, 0]}>
            {chartData.map((entry, i) => (
              <Cell key={i} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
