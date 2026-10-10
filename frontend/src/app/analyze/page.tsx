"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ResumeUploader from "@/components/ResumeUploader";
import JDInput from "@/components/JDInput";
import ScoreRing from "@/components/ScoreRing";
import KeywordTable from "@/components/KeywordTable";
import BulletRewriter from "@/components/BulletRewriter";
import RedFlagCards from "@/components/RedFlagCards";
import CoverLetterPanel from "@/components/CoverLetterPanel";
import ATSSimulationView from "@/components/ATSSimulation";
import FadeIn from "@/components/animations/FadeIn";
import { analyzeResume } from "@/lib/api";
import { AnalysisResponse, AnalysisStatus } from "@/types";
import { getScoreColor, getScoreBgColor, formatDuration } from "@/lib/utils";
import {
  Loader2,
  Target,
  Search,
  PenLine,
  AlertTriangle,
  FileText,
  Monitor,
  BarChart3,
  ArrowLeft,
} from "lucide-react";

const pageTransition = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
  transition: { duration: 0.4 },
};

export default function AnalyzePage() {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [jobUrl, setJobUrl] = useState("");
  const [status, setStatus] = useState<AnalysisStatus>("idle");
  const [progress, setProgress] = useState(0);
  const [progressMessage, setProgressMessage] = useState("");
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState("overview");

  const canAnalyze =
    resumeFile && (jobDescription.trim().length > 50 || jobUrl.trim().length > 10);

  const handleAnalyze = async () => {
    if (!resumeFile || (!jobDescription && !jobUrl)) return;

    setStatus("analyzing");
    setError(null);
    setResult(null);
    setProgress(0);

    try {
      const response = await analyzeResume(
        resumeFile,
        jobDescription,
        jobUrl || undefined,
        (p, msg) => {
          setProgress(p);
          setProgressMessage(msg);
        }
      );
      setResult(response);
      setStatus("complete");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : String(err));
      setStatus("error");
    }
  };

  const tabs = [
    { id: "overview", label: "Overview", icon: BarChart3 },
    { id: "keywords", label: "Keywords", icon: Search },
    { id: "rewrites", label: "Rewrites", icon: PenLine },
    { id: "redflags", label: "Red Flags", icon: AlertTriangle },
    { id: "coverletter", label: "Cover Letter", icon: FileText },
    { id: "ats", label: "ATS Sim", icon: Monitor },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <AnimatePresence mode="wait">
        {/* ==================== INPUT PHASE ==================== */}
        {status !== "complete" && (
          <motion.div
            key="input"
            {...pageTransition}
            className="max-w-4xl mx-auto"
          >
            <FadeIn>
              <h1 className="text-3xl md:text-4xl font-bold mb-2">
                Analyze Your{" "}
                <span className="animate-gradient-text">Resume</span>
              </h1>
              <p className="text-slate-400 mb-10">
                Upload your resume and paste the job description to get started.
              </p>
            </FadeIn>

            <div className="grid md:grid-cols-2 gap-8">
              <FadeIn direction="left" delay={0.2}>
                <div>
                  <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                    <motion.div
                      animate={{ rotate: [0, 10, -10, 0] }}
                      transition={{ repeat: Infinity, duration: 4, repeatDelay: 2 }}
                    >
                      <FileText className="h-5 w-5 text-blue-400" />
                    </motion.div>
                    Your Resume
                  </h2>
                  <ResumeUploader
                    onFileSelect={setResumeFile}
                    selectedFile={resumeFile}
                  />
                </div>
              </FadeIn>

              <FadeIn direction="right" delay={0.3}>
                <div>
                  <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                    <motion.div
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ repeat: Infinity, duration: 3, repeatDelay: 2 }}
                    >
                      <Target className="h-5 w-5 text-blue-400" />
                    </motion.div>
                    Job Description
                  </h2>
                  <JDInput
                    value={jobDescription}
                    onChange={setJobDescription}
                    jobUrl={jobUrl}
                    onUrlChange={setJobUrl}
                  />
                </div>
              </FadeIn>
            </div>

            {/* Analyze Button */}
            <div className="mt-10 text-center">
              {status === "analyzing" ? (
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="space-y-6"
                >
                  {/* Spinning loader */}
                  <div className="flex items-center justify-center gap-3">
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
                    >
                      <Loader2 className="h-7 w-7 text-blue-500" />
                    </motion.div>
                    <AnimatePresence mode="wait">
                      <motion.span
                        key={progressMessage}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="text-white font-medium text-lg"
                      >
                        {progressMessage || "Analyzing..."}
                      </motion.span>
                    </AnimatePresence>
                  </div>

                  {/* Progress bar with shimmer */}
                  <div className="max-w-md mx-auto">
                    <div className="h-3 bg-slate-800 rounded-full overflow-hidden">
                      <motion.div
                        className="h-full rounded-full animate-shimmer"
                        initial={{ width: 0 }}
                        animate={{ width: `${progress}%` }}
                        transition={{ duration: 0.5, ease: "easeOut" }}
                      />
                    </div>
                    <p className="text-slate-500 text-sm mt-3">
                      {Math.round(progress)}% complete
                    </p>
                  </div>

                  {/* Fun fact while waiting */}
                  <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 3 }}
                    className="text-slate-600 text-sm max-w-sm mx-auto"
                  >
                    💡 Fun fact: 75% of resumes are rejected by ATS before a
                    human ever reads them.
                  </motion.p>
                </motion.div>
              ) : (
                <motion.div
                  whileHover={canAnalyze ? { scale: 1.05 } : {}}
                  whileTap={canAnalyze ? { scale: 0.95 } : {}}
                >
                  <button
                    onClick={handleAnalyze}
                    disabled={!canAnalyze}
                    className={`px-10 py-4 rounded-xl text-lg font-semibold transition-all ${
                      canAnalyze
                        ? "bg-blue-600 hover:bg-blue-700 text-white animate-glow-pulse"
                        : "bg-slate-800 text-slate-500 cursor-not-allowed"
                    }`}
                  >
                    {status === "error" ? "Try Again" : "Analyze Resume"}
                  </button>
                </motion.div>
              )}

              {/* Error message */}
              <AnimatePresence>
                {error && (
                  <motion.div
                    initial={{ opacity: 0, y: 10, height: 0 }}
                    animate={{ opacity: 1, y: 0, height: "auto" }}
                    exit={{ opacity: 0, y: -10, height: 0 }}
                    className="mt-4 p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 max-w-md mx-auto"
                  >
                    {error}
                  </motion.div>
                )}
              </AnimatePresence>

              {!canAnalyze && status === "idle" && (
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 1 }}
                  className="text-slate-600 text-sm mt-4"
                >
                  Upload a resume and enter at least 50 characters of job
                  description to start.
                </motion.p>
              )}
            </div>
          </motion.div>
        )}

        {/* ==================== RESULTS PHASE ==================== */}
        {status === "complete" && result && (
          <motion.div key="results" {...pageTransition}>
            {/* Header */}
            <div className="flex items-center justify-between mb-8">
              <FadeIn>
                <div>
                  <h1 className="text-3xl font-bold">
                    Analysis{" "}
                    <span className="animate-gradient-text">Results</span>
                  </h1>
                  <p className="text-slate-400 mt-1">
                    Completed in{" "}
                    {formatDuration(result.metadata.analysis_time_ms)} using{" "}
                    {result.metadata.llm_model}
                  </p>
                </div>
              </FadeIn>

              <FadeIn delay={0.2}>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => {
                    setStatus("idle");
                    setResult(null);
                  }}
                  className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm text-white transition-colors"
                >
                  <ArrowLeft className="h-4 w-4" />
                  New Analysis
                </motion.button>
              </FadeIn>
            </div>

            {/* Score + Category Summary */}
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              {/* Main Score */}
              <FadeIn delay={0.2}>
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 flex justify-center backdrop-blur-sm"
                >
                  <ScoreRing score={result.overall_score} />
                </motion.div>
              </FadeIn>

              {/* Category Scores */}
              <FadeIn delay={0.4} className="md:col-span-2">
                <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm h-full">
                  <h3 className="text-lg font-semibold mb-5">
                    Score Breakdown
                  </h3>
                  <div className="space-y-5">
                    {[
                      {
                        label: "Skills Match",
                        score: result.category_scores.skills_match.score,
                        weight: "40%",
                      },
                      {
                        label: "Experience",
                        score: result.category_scores.experience_match.score,
                        weight: "30%",
                      },
                      {
                        label: "Education",
                        score: result.category_scores.education_match.score,
                        weight: "15%",
                      },
                      {
                        label: "Keywords",
                        score: result.category_scores.keyword_density.score,
                        weight: "15%",
                      },
                    ].map((cat, i) => (
                      <motion.div
                        key={cat.label}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.6 + i * 0.15 }}
                      >
                        <div className="flex justify-between mb-1.5">
                          <span className="text-slate-300 text-sm">
                            {cat.label}{" "}
                            <span className="text-slate-600">
                              ({cat.weight})
                            </span>
                          </span>
                          <motion.span
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: 0.8 + i * 0.15 }}
                            className={`font-bold ${getScoreColor(cat.score)}`}
                          >
                            {cat.score}/100
                          </motion.span>
                        </div>
                        <div className="h-2.5 bg-slate-800 rounded-full overflow-hidden">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${cat.score}%` }}
                            transition={{
                              delay: 0.7 + i * 0.15,
                              duration: 1,
                              ease: "easeOut",
                            }}
                            className={`h-full rounded-full ${getScoreBgColor(
                              cat.score
                            )}`}
                          />
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </FadeIn>
            </div>

            {/* Tabs */}
            <FadeIn delay={0.6}>
              <div className="border-b border-slate-800 mb-6">
                <div className="flex gap-1 overflow-x-auto">
                  {tabs.map((tab) => (
                    <motion.button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      whileHover={{ y: -2 }}
                      whileTap={{ scale: 0.95 }}
                      className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ${
                        activeTab === tab.id
                          ? "border-blue-500 text-blue-400"
                          : "border-transparent text-slate-400 hover:text-white"
                      }`}
                    >
                      <tab.icon className="h-4 w-4" />
                      {tab.label}
                      {tab.id === "redflags" &&
                        result.red_flags.length > 0 && (
                          <motion.span
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            className="bg-red-500/20 text-red-400 text-xs px-1.5 py-0.5 rounded-full"
                          >
                            {result.red_flags.length}
                          </motion.span>
                        )}
                      {tab.id === "keywords" &&
                        result.missing_keywords.length > 0 && (
                          <motion.span
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            className="bg-yellow-500/20 text-yellow-400 text-xs px-1.5 py-0.5 rounded-full"
                          >
                            {result.missing_keywords.length}
                          </motion.span>
                        )}
                    </motion.button>
                  ))}
                </div>
              </div>
            </FadeIn>

            {/* Tab Content with AnimatePresence for transitions */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm min-h-100">
              <AnimatePresence mode="wait">
                <motion.div
                  key={activeTab}
                  initial={{ opacity: 0, y: 15, filter: "blur(4px)" }}
                  animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
                  exit={{ opacity: 0, y: -15, filter: "blur(4px)" }}
                  transition={{ duration: 0.3 }}
                >
                  {activeTab === "overview" && (
                    <div className="space-y-6">
                      {[
                        {
                          label: "Skills Match",
                          details:
                            result.category_scores.skills_match.details,
                        },
                        {
                          label: "Experience",
                          details:
                            result.category_scores.experience_match.details,
                        },
                        {
                          label: "Education",
                          details:
                            result.category_scores.education_match.details,
                        },
                        {
                          label: "Keyword Optimization",
                          details:
                            result.category_scores.keyword_density.details,
                        },
                      ].map((item, i) => (
                        <motion.div
                          key={item.label}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: i * 0.1 }}
                          className="p-4 bg-slate-800/30 rounded-xl border border-slate-700/50"
                        >
                          <h3 className="text-white font-semibold mb-1">
                            {item.label}
                          </h3>
                          <p className="text-slate-400">{item.details}</p>
                        </motion.div>
                      ))}
                    </div>
                  )}

                  {activeTab === "keywords" && (
                    <KeywordTable
                      skillsMatch={result.category_scores.skills_match}
                      missingKeywords={result.missing_keywords}
                    />
                  )}

                  {activeTab === "rewrites" && (
                    <BulletRewriter rewrites={result.bullet_rewrites} />
                  )}

                  {activeTab === "redflags" && (
                    <RedFlagCards flags={result.red_flags} />
                  )}

                  {activeTab === "coverletter" && (
                    <CoverLetterPanel content={result.cover_letter} />
                  )}

                  {activeTab === "ats" && result.ats_simulation && (
                    <ATSSimulationView data={result.ats_simulation} />
                  )}
                </motion.div>
              </AnimatePresence>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}