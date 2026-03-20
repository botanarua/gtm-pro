"use client";

import { SalesPitch } from "@/lib/types";

export default function PitchCard({ data }: { data: SalesPitch }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <h3 className="font-semibold text-lg mb-4">Pitch de vendas</h3>
      <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4 mb-4">
        <p className="text-xl font-bold text-indigo-900 mb-1">{data.headline}</p>
        <p className="text-sm text-indigo-700 mb-3">{data.subheadline}</p>
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium">
          {data.cta}
        </button>
      </div>
      <p className="text-sm text-gray-600 mb-3">{data.why_this_message}</p>
      {data.angles.length > 0 && (
        <div>
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Ângulos</p>
          <ul className="space-y-1">
            {data.angles.map((angle, i) => (
              <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                <span className="text-indigo-500 mt-0.5">&#8226;</span>
                {angle}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
