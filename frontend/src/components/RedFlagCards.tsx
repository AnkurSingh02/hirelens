"use client";

import { RedFlag } from "@/types";
import { AlertTriangle, AlertCircle, Info } from "lucide-react";
import { getSeverityColor } from "@/lib/utils";

interface RedFlagCardsProps {
  flags: RedFlag[];
}

export default function RedFlagCards({ flags }: RedFlagCardsProps) {
  if (flags.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-green-400 font-medium">
          ✅ No major red flags detected!
        </p>
      </div>
    );
  }

  const getIcon = (severity: string) => {
    switch (severity) {
      case "high":
        return <AlertTriangle className="h-5 w-5" />;
      case "medium":
        return <AlertCircle className="h-5 w-5" />;
      default:
        return <Info className="h-5 w-5" />;
    }
  };

  return (
    <div className="space-y-3">
      {flags.map((flag, i) => (
        <div
          key={i}
          className={`border rounded-xl p-4 ${getSeverityColor(flag.severity)}`}
        >
          <div className="flex items-start gap-3">
            <div className="mt-0.5 shrink-0">{getIcon(flag.severity)}</div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="font-semibold capitalize">{flag.type.replace(/_/g, " ")}</span>
                <span className="text-xs uppercase font-bold opacity-75">
                  {flag.severity}
                </span>
              </div>
              <p className="text-sm opacity-90">{flag.message}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}