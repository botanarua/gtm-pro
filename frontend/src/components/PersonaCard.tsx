"use client";

import { Persona } from "@/lib/types";

function TagList({ title, items }: { title: string; items: string[] }) {
  if (!items.length) return null;
  return (
    <div>
      <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">{title}</p>
      <div className="flex flex-wrap gap-1.5">
        {items.map((item, i) => (
          <span key={i} className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded-md">{item}</span>
        ))}
      </div>
    </div>
  );
}

export default function PersonaCard({ data }: { data: Persona }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <h3 className="font-semibold text-lg mb-1">Persona JTBD</h3>
      <p className="text-xl font-bold text-indigo-700 mb-1">{data.persona_name}</p>
      <p className="text-sm text-gray-600 mb-4">{data.contexto_de_busca}</p>
      <div className="space-y-3">
        <TagList title="Jobs Funcionais" items={data.job_functional} />
        <TagList title="Jobs Emocionais" items={data.job_emotional} />
        <TagList title="Jobs Sociais" items={data.job_social} />
        <TagList title="Necessidades urgentes" items={data.necessidades_urgentes} />
        <TagList title="Objeções" items={data.principais_objecoes} />
        <TagList title="Gatilhos de ação" items={data.gatilhos_de_acao} />
      </div>
    </div>
  );
}
