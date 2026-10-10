"use client";

import { useState } from "react";
import { Link2, FileText } from "lucide-react";

interface JDInputProps {
  value: string;
  onChange: (value: string) => void;
  jobUrl: string;
  onUrlChange: (url: string) => void;
}

export default function JDInput({
  value,
  onChange,
  jobUrl,
  onUrlChange,
}: JDInputProps) {
  const [mode, setMode] = useState<"paste" | "url">("paste");

  return (
    <div className="space-y-4">
      {/* Toggle */}
      <div className="flex gap-2">
        <button
          onClick={() => setMode("paste")}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            mode === "paste"
              ? "bg-blue-600 text-white"
              : "bg-slate-800 text-slate-400 hover:text-white"
          }`}
        >
          <FileText className="h-4 w-4" />
          Paste Text
        </button>
        <button
          onClick={() => setMode("url")}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            mode === "url"
              ? "bg-blue-600 text-white"
              : "bg-slate-800 text-slate-400 hover:text-white"
          }`}
        >
          <Link2 className="h-4 w-4" />
          Job URL
        </button>
      </div>

      {/* Input */}
      {mode === "paste" ? (
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Paste the full job description here...

Example:
We are looking for a Senior Software Engineer to join our team.

Requirements:
- 5+ years experience with Python
- Experience with React and TypeScript
- Strong understanding of REST APIs
..."
          className="w-full h-64 bg-slate-800/50 border border-slate-700 rounded-xl p-4 text-white placeholder-slate-500 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      ) : (
        <div className="space-y-2">
          <input
            type="url"
            value={jobUrl}
            onChange={(e) => onUrlChange(e.target.value)}
            placeholder="https://www.linkedin.com/jobs/view/..."
            className="w-full bg-slate-800/50 border border-slate-700 rounded-xl p-4 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p className="text-slate-500 text-sm">
            Supports LinkedIn, Indeed, and most job posting pages.
            Some pages may require you to paste the text directly.
          </p>
        </div>
      )}
    </div>
  );
}