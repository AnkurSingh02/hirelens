import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getScoreColor(score: number): string {
  if (score >= 80) return "text-green-500";
  if (score >= 60) return "text-yellow-500";
  if (score >= 40) return "text-orange-500";
  return "text-red-500";
}

export function getScoreBgColor(score: number): string {
  if (score >= 80) return "bg-green-500";
  if (score >= 60) return "bg-yellow-500";
  if (score >= 40) return "bg-orange-500";
  return "bg-red-500";
}

export function getScoreLabel(score: number): string {
  if (score >= 80) return "Excellent Match";
  if (score >= 60) return "Good Match";
  if (score >= 40) return "Needs Improvement";
  return "Poor Match";
}

export function getSeverityColor(severity: string): string {
  switch (severity) {
    case "high":
      return "border-red-500 bg-red-500/10 text-red-400";
    case "medium":
      return "border-yellow-500 bg-yellow-500/10 text-yellow-400";
    case "low":
      return "border-blue-500 bg-blue-500/10 text-blue-400";
    default:
      return "border-gray-500 bg-gray-500/10 text-gray-400";
  }
}

export function getStatusIcon(status: string): string {
  switch (status) {
    case "parsed":
      return "✅";
    case "partial":
      return "⚠️";
    case "failed":
      return "❌";
    default:
      return "❓";
  }
}

export function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  return `${(ms / 1000).toFixed(1)}s`;
}