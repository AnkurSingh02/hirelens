"use client";

import { motion } from "framer-motion";
import { getScoreColor, getScoreLabel } from "@/lib/utils";
import AnimatedCounter from "@/components/animations/AnimatedCounter";

interface ScoreRingProps {
  score: number;
  size?: number;
  strokeWidth?: number;
}

export default function ScoreRing({
  score,
  size = 200,
  strokeWidth = 12,
}: ScoreRingProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (score / 100) * circumference;

  const strokeColor =
    score >= 80
      ? "#22c55e"
      : score >= 60
      ? "#eab308"
      : score >= 40
      ? "#f97316"
      : "#ef4444";

  const glowColor =
    score >= 80
      ? "rgba(34,197,94,0.3)"
      : score >= 60
      ? "rgba(234,179,8,0.3)"
      : score >= 40
      ? "rgba(249,115,22,0.3)"
      : "rgba(239,68,68,0.3)";

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform -rotate-90">
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#1e293b"
            strokeWidth={strokeWidth}
            fill="none"
          />
          {/* Animated score circle */}
          <motion.circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            fill="none"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.5, ease: "easeOut", delay: 0.3 }}
            style={{
              filter: `drop-shadow(0 0 8px ${glowColor})`,
            }}
          />
        </svg>

        {/* Score number */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <AnimatedCounter
            value={score}
            className={`text-5xl font-bold ${getScoreColor(score)}`}
            duration={1.5}
          />
          <span className="text-slate-500 text-sm">/100</span>
        </div>
      </div>

      <motion.p
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.5 }}
        className={`font-semibold text-lg ${getScoreColor(score)}`}
      >
        {getScoreLabel(score)}
      </motion.p>
    </div>
  );
}