"use client";

import { AcquisitionExperiment } from "@/lib/types";

const clusterColors: Record<string, string> = {
  awareness: "bg-blue-100 text-blue-800 border-blue-200",
  consideration: "bg-yellow-100 text-yellow-800 border-yellow-200",
  action: "bg-green-100 text-green-800 border-green-200",
};

export default function ExperimentPlan({ data }: { data: AcquisitionExperiment }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <h3 className="font-semibold text-lg mb-1">Experimento de aquisição</h3>
      <div className="flex gap-4 text-sm text-gray-600 mb-4">
        <span>Google Ads {data.campaign_type}</span>
        <span>R${data.budget_recommended.toFixed(0)} budget</span>
        <span>{data.duration_days} dias</span>
      </div>
      <div className="space-y-4">
        {data.campaign_structure.map((group, i) => (
          <div key={i} className={`border rounded-lg p-4 ${clusterColors[group.cluster] || "border-gray-200"}`}>
            <div className="flex items-center gap-2 mb-2">
              <span className="font-semibold text-sm uppercase">{group.cluster}</span>
            </div>
            <p className="text-sm mb-2">{group.message}</p>
            <div className="flex flex-wrap gap-1.5">
              {group.keywords.map((kw, j) => (
                <span key={j} className="bg-white/60 text-xs px-2 py-0.5 rounded border border-current/10">
                  {kw}
                </span>
              ))}
            </div>
            {group.responsive_ad_headlines.length > 0 && (
              <div className="mt-3 pt-3 border-t border-current/10">
                <p className="text-xs font-semibold mb-1 opacity-70">Headlines</p>
                <div className="flex flex-wrap gap-1">
                  {group.responsive_ad_headlines.map((h, j) => (
                    <span key={j} className="text-xs bg-white/50 px-2 py-0.5 rounded">{h}</span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
