"use client";

interface Props {
  label: "testar" | "testar_com_cautela" | "nao_testar";
  score: number;
}

const config = {
  testar: { text: "TESTAR", bg: "bg-green-100", color: "text-green-800", border: "border-green-300" },
  testar_com_cautela: { text: "TESTAR COM CAUTELA", bg: "bg-yellow-100", color: "text-yellow-800", border: "border-yellow-300" },
  nao_testar: { text: "NÃO TESTAR", bg: "bg-red-100", color: "text-red-800", border: "border-red-300" },
};

export default function DiagnosisBadge({ label, score }: Props) {
  const c = config[label];
  return (
    <div className={`inline-flex items-center gap-3 px-4 py-2 rounded-full border ${c.bg} ${c.border}`}>
      <span className={`font-bold text-sm ${c.color}`}>{c.text}</span>
      <span className={`text-sm ${c.color} opacity-75`}>Score: {score.toFixed(2)}</span>
    </div>
  );
}
