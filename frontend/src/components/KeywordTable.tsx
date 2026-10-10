"use client";

import { motion } from "framer-motion";
import { MissingKeyword, CategoryScore } from "@/types";
import { CheckCircle, XCircle, AlertCircle } from "lucide-react";

interface KeywordTableProps {
  skillsMatch: CategoryScore;
  missingKeywords: MissingKeyword[];
}

export default function KeywordTable({
  skillsMatch,
  missingKeywords,
}: KeywordTableProps) {
  const importanceColor = {
    high: "text-red-400 bg-red-500/10 border-red-500/30",
    medium: "text-yellow-400 bg-yellow-500/10 border-yellow-500/30",
    low: "text-blue-400 bg-blue-500/10 border-blue-500/30",
  };

  return (
    <div className="space-y-8">
      {/* Matched Keywords */}
      {skillsMatch.matched.length > 0 && (
        <div>
          <motion.h3
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="text-green-400 font-semibold mb-4 flex items-center gap-2"
          >
            <CheckCircle className="h-5 w-5" />
            Found in Your Resume ({skillsMatch.matched.length})
          </motion.h3>
          <div className="flex flex-wrap gap-2">
            {skillsMatch.matched.map((keyword, i) => (
              <motion.span
                key={i}
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{
                  delay: i * 0.05,
                  type: "spring",
                  stiffness: 300,
                }}
                className="px-3 py-1.5 bg-green-500/10 border border-green-500/30 rounded-full text-green-400 text-sm"
              >
                {keyword}
              </motion.span>
            ))}
          </div>
        </div>
      )}

      {/* Missing Keywords */}
      {missingKeywords.length > 0 && (
        <div>
          <motion.h3
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="text-red-400 font-semibold mb-4 flex items-center gap-2"
          >
            <XCircle className="h-5 w-5" />
            Missing from Your Resume ({missingKeywords.length})
          </motion.h3>
          <div className="space-y-2">
            {missingKeywords.map((kw, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 + i * 0.08 }}
                whileHover={{ x: 4 }}
                className="flex items-start gap-3 p-3 bg-slate-800/50 rounded-lg border border-slate-700 cursor-default"
              >
                <span
                  className={`px-2 py-0.5 rounded text-xs font-medium border shrink-0 ${
                    importanceColor[kw.importance]
                  }`}
                >
                  {kw.importance}
                </span>
                <div>
                  <span className="text-white font-medium">{kw.keyword}</span>
                  <p className="text-slate-400 text-sm mt-1">{kw.context}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Details */}
      {skillsMatch.details && skillsMatch.details.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-xl border border-slate-700 bg-slate-900/60 p-4"
        >
          <h4 className="mb-3 flex items-center gap-2 text-sm font-semibold text-slate-200">
            <AlertCircle className="h-4 w-4 text-sky-400" />
            Match Details
          </h4>
          <p className="text-sm text-slate-300">{skillsMatch.details}</p>
        </motion.div>
      )}
    </div>
  );
}
