"use client";

import { useState } from "react";
import { Copy, Check, Download } from "lucide-react";

interface CoverLetterPanelProps {
  content: string;
}

export default function CoverLetterPanel({ content }: CoverLetterPanelProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!content) {
    return (
      <p className="text-slate-400 text-center py-8">
        No cover letter generated.
      </p>
    );
  }

  return (
    <div className="space-y-4">
      {/* Actions */}
      <div className="flex gap-2 justify-end">
        <button
          onClick={handleCopy}
          className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm text-white transition-colors"
        >
          {copied ? (
            <>
              <Check className="h-4 w-4 text-green-400" /> Copied!
            </>
          ) : (
            <>
              <Copy className="h-4 w-4" /> Copy
            </>
          )}
        </button>
      </div>

      {/* Content */}
      <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-6">
        <div className="prose prose-invert max-w-none">
          {content.split("\n").map((paragraph, i) => (
            <p key={i} className="text-slate-300 mb-4 leading-relaxed">
              {paragraph}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
}