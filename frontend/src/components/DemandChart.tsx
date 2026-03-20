"use client";

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { SearchDemand } from "@/lib/types";

const COLORS = { awareness: "#93c5fd", consideration: "#fbbf24", action: "#34d399" };

export default function DemandChart({ data }: { data: SearchDemand }) {
  const ct = data.cluster_totals;
  const total = ct.awareness + ct.consideration + ct.action;

  const chartData = [
    { name: "Awareness", value: ct.awareness, color: COLORS.awareness },
    { name: "Consideration", value: ct.consideration, color: COLORS.consideration },
    { name: "Action", value: ct.action, color: COLORS.action },
  ];

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <h3 className="font-semibold text-lg mb-1">Demanda de busca</h3>
      <p className="text-3xl font-bold text-gray-900 mb-1">{total.toLocaleString("pt-BR")}<span className="text-base font-normal text-gray-500">/mês</span></p>
      <p className="text-sm text-gray-500 mb-4">{data.keywords.length} keywords analisadas</p>
      <ResponsiveContainer width="100%" height={180}>
        <BarChart data={chartData} layout="vertical" margin={{ left: 10 }}>
          <XAxis type="number" tickFormatter={(v) => v.toLocaleString("pt-BR")} fontSize={12} />
          <YAxis type="category" dataKey="name" width={100} fontSize={12} />
          <Tooltip formatter={(v: number) => v.toLocaleString("pt-BR")} />
          <Bar dataKey="value" radius={[0, 6, 6, 0]}>
            {chartData.map((entry, i) => (
              <Cell key={i} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
