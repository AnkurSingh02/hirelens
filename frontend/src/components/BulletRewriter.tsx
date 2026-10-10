"use client";

import { BulletRewrite } from "@/types";
import { ArrowRight, Lightbulb } from "lucide-react";

interface BulletRewriterProps {
  rewrites: BulletRewrite[];
}

export default function BulletRewriter({ rewrites }: BulletRewriterProps) {
  if (rewrites.length === 0) {
    return (
      <p className="text-slate-400 text-center py-8">
        No bullet rewrites generated.
      </p>
    );
  }

  return (
    <div className="space-y-6">
      {rewrites.map((rewrite, i) => (
        <div
          key={i}
          className="border border-slate-700 rounded-xl overflow-hidden"
        >
          {/* Original vs Rewritten */}
          <div className="grid md:grid-cols-2 divide-x divide-slate-700">
            {/* Original */}
            <div className="p-4">
              <p className="text-xs font-semibold text-red-400 uppercase tracking-wider mb-2">
                Original
              </p>
              <p className="text-slate-300">{rewrite.original}</p>
            </div>

            {/* Rewritten */}
            <div className="p-4 bg-green-500/5">
              <p className="text-xs font-semibold text-green-400 uppercase tracking-wider mb-2">
                ✨ Optimized
              </p>
              <p className="text-white">{rewrite.rewritten}</p>
            </div>
          </div>

          {/* Reasoning */}
          <div className="px-4 py-3 bg-slate-800/50 border-t border-slate-700">
            <div className="flex items-start gap-2">
              <Lightbulb className="h-4 w-4 text-yellow-400 mt-0.5 shrink-0" />
              <p className="text-slate-400 text-sm">{rewrite.reasoning}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}