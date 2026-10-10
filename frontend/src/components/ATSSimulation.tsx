"use client";

import { ATSSimulation as ATSSimType } from "@/types";
import { getStatusIcon } from "@/lib/utils";
import { Eye, AlertTriangle } from "lucide-react";

interface ATSSimulationProps {
  data: ATSSimType;
}

export default function ATSSimulation({ data }: ATSSimulationProps) {
  return (
    <div className="space-y-6">
      {/* Parsed Contact Info */}
      <div>
        <h3 className="text-white font-semibold mb-3">Detected Contact Info</h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700">
            <p className="text-slate-400 text-xs mb-1">Name</p>
            <p className="text-white text-sm">
              {data.parsed_name || "❌ Not detected"}
            </p>
          </div>
          <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700">
            <p className="text-slate-400 text-xs mb-1">Email</p>
            <p className="text-white text-sm">
              {data.parsed_email || "❌ Not detected"}
            </p>
          </div>
          <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700">
            <p className="text-slate-400 text-xs mb-1">Phone</p>
            <p className="text-white text-sm">
              {data.parsed_phone || "❌ Not detected"}
            </p>
          </div>
        </div>
      </div>

      {/* Section Parsing Results */}
      <div>
        <h3 className="text-white font-semibold mb-3">Section Parsing</h3>
        <div className="space-y-2">
          {data.sections.map((section, i) => (
            <div
              key={i}
              className="flex items-start gap-3 p-3 bg-slate-800/50 rounded-lg border border-slate-700"
            >
              <span className="text-lg">{getStatusIcon(section.status)}</span>
              <div>
                <span className="text-white font-medium">
                  {section.section_name}
                </span>
                <p className="text-slate-400 text-sm">{section.message}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Formatting Issues */}
      {data.formatting_issues.length > 0 && (
        <div>
          <h3 className="text-yellow-400 font-semibold mb-3 flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" />
            Formatting Issues
          </h3>
          <div className="space-y-2">
            {data.formatting_issues.map((issue, i) => (
              <div
                key={i}
                className="p-3 bg-yellow-500/10 border border-yellow-500/30 rounded-lg text-yellow-300 text-sm"
              >
                {issue}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Raw Text Preview */}
      <div>
        <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
          <Eye className="h-5 w-5" />
          What the ATS Sees (Raw Text)
        </h3>
        <pre className="bg-black/50 border border-slate-700 rounded-xl p-4 text-slate-400 text-xs font-mono overflow-x-auto max-h-64 overflow-y-auto whitespace-pre-wrap">
          {data.raw_text_preview}
        </pre>
      </div>
    </div>
  );
}