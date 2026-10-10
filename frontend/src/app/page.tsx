"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  Target,
  Zap,
  Shield,
  FileText,
  ArrowRight,
  CheckCircle,
  Sparkles,
} from "lucide-react";
import FadeIn from "@/components/animations/FadeIn";
import StaggerContainer, {
  StaggerItem,
} from "@/components/animations/StaggerContainer";
import TypewriterText from "@/components/animations/TypewriterText";

const features = [
  {
    icon: Target,
    title: "Match Score (0-100)",
    description:
      "Detailed breakdown by skills, experience, education, and keyword density.",
    color: "from-blue-500 to-cyan-500",
  },
  {
    icon: Zap,
    title: "Missing Keywords",
    description:
      "See exactly which ATS keywords you're missing and how important they are.",
    color: "from-yellow-500 to-orange-500",
  },
  {
    icon: FileText,
    title: "Bullet Rewrites",
    description:
      "AI rewrites your bullet points to match the job description using the XYZ formula.",
    color: "from-green-500 to-emerald-500",
  },
  {
    icon: Shield,
    title: "ATS Simulation",
    description:
      "See your resume the way an ATS parser sees it — most formatting breaks silently.",
    color: "from-purple-500 to-pink-500",
  },
];

const stats = [
  { value: "94%", label: "Keyword Accuracy" },
  { value: "30s", label: "Analysis Time" },
  { value: "$0", label: "Forever Free" },
  { value: "0", label: "API Keys Needed" },
];

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* ==================== HERO ==================== */}
      <section className="max-w-7xl mx-auto px-4 pt-24 pb-20 text-center relative">
        {/* Decorative spinning ring */}
        <div className="absolute top-10 left-1/2 -translate-x-1/2 w-150 h-150 border border-blue-500/10 rounded-full animate-spin-slow pointer-events-none" />
        <div className="absolute top-20 left-1/2 -translate-x-1/2 w-100 h-100 border border-purple-500/10 rounded-full animate-spin-slow pointer-events-none" style={{ animationDirection: "reverse", animationDuration: "30s" }} />

        {/* Badge */}
        <FadeIn delay={0.2}>
          <motion.div
            className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/30 rounded-full px-5 py-2 mb-8"
            whileHover={{ scale: 1.05 }}
          >
            <Sparkles className="h-4 w-4 text-blue-400 animate-float" />
            <span className="text-blue-400 text-sm font-medium">
              Powered by Llama 3.3 70B — 100% Free
            </span>
          </motion.div>
        </FadeIn>

        {/* Main heading with stagger */}
        <h1 className="text-5xl md:text-7xl font-bold mb-6 tracking-tight">
          <motion.span
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.6 }}
            className="block"
          >
            Stop Getting
          </motion.span>
          <motion.span
            initial={{ opacity: 0, y: 30, filter: "blur(10px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            transition={{ delay: 0.7, duration: 0.8 }}
            className="animate-gradient-text block"
          >
            Ghosted by ATS
          </motion.span>
        </h1>

        {/* Subtitle with typewriter */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
          className="text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed"
        >
          <TypewriterText
            text="Upload your resume + paste any job description. HireLens tells you exactly why you're getting rejected and how to fix it — in 30 seconds."
            delay={1.3}
            speed={0.02}
          />
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.8 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Link
              href="/analyze"
              className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl text-lg font-semibold animate-glow-pulse transition-colors"
            >
              Analyze Your Resume
              <motion.span
                animate={{ x: [0, 5, 0] }}
                transition={{ repeat: Infinity, duration: 1.5 }}
              >
                <ArrowRight className="h-5 w-5" />
              </motion.span>
            </Link>
          </motion.div>

          <motion.a
            href="https://github.com"
            target="_blank"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="inline-flex items-center gap-2 bg-slate-800/50 hover:bg-slate-800 border border-slate-700 text-slate-300 px-8 py-4 rounded-xl text-lg font-medium transition-colors"
          >
            View on GitHub
          </motion.a>
        </motion.div>

        {/* Stats bar */}
        <FadeIn delay={2.2}>
          <div className="flex items-center justify-center gap-8 md:gap-16 mt-16 pt-8 border-t border-slate-800/50">
            {stats.map((stat, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 2.4 + i * 0.1 }}
                className="text-center"
              >
                <p className="text-2xl md:text-3xl font-bold text-white">
                  {stat.value}
                </p>
                <p className="text-slate-500 text-sm mt-1">{stat.label}</p>
              </motion.div>
            ))}
          </div>
        </FadeIn>
      </section>

      {/* ==================== FEATURES ==================== */}
      <section className="max-w-7xl mx-auto px-4 py-24">
        <FadeIn>
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">
            Everything You Need to{" "}
            <span className="animate-gradient-text">Beat the ATS</span>
          </h2>
          <p className="text-slate-400 text-center max-w-xl mx-auto mb-16">
            Recruiters spend 6 seconds per resume. ATS systems spend 0. Make
            every second count.
          </p>
        </FadeIn>

        <StaggerContainer staggerDelay={0.15} className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, i) => (
            <StaggerItem key={i}>
              <motion.div
                whileHover={{ y: -8, scale: 1.02 }}
                transition={{ type: "spring", stiffness: 300 }}
                className="card-glow bg-slate-900/50 border border-slate-800 rounded-2xl p-6 h-full cursor-default"
              >
                {/* Icon with gradient background */}
                <div
                  className={`w-12 h-12 rounded-xl bg-linear-to-br ${feature.color} flex items-center justify-center mb-4 shadow-lg`}
                >
                  <feature.icon className="h-6 w-6 text-white" />
                </div>

                <h3 className="text-white font-semibold text-lg mb-2">
                  {feature.title}
                </h3>
                <p className="text-slate-400 text-sm leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            </StaggerItem>
          ))}
        </StaggerContainer>
      </section>

      {/* ==================== HOW IT WORKS ==================== */}
      <section className="max-w-4xl mx-auto px-4 py-24">
        <FadeIn>
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">
            Three Steps. Thirty Seconds.
          </h2>
        </FadeIn>

        <div className="space-y-12">
          {[
            {
              step: "01",
              title: "Paste the Job Description",
              desc: "Copy from LinkedIn, Indeed, or any job posting. You can also paste a URL and we'll scrape it.",
              color: "from-blue-500 to-cyan-500",
            },
            {
              step: "02",
              title: "Upload Your Resume",
              desc: "Drag and drop your PDF resume. We parse it instantly — no signup, no email, no nonsense.",
              color: "from-purple-500 to-pink-500",
            },
            {
              step: "03",
              title: "Get Your Full Analysis",
              desc: "Match score, missing keywords, bullet rewrites, red flags, cover letter, and ATS simulation.",
              color: "from-green-500 to-emerald-500",
            },
          ].map((item, i) => (
            <FadeIn key={i} direction={i % 2 === 0 ? "left" : "right"} delay={i * 0.2}>
              <motion.div
                whileHover={{ x: 8 }}
                className="flex items-start gap-8 group"
              >
                {/* Step number */}
                <div
                  className={`shrink-0 w-16 h-16 bg-linear-to-br ${item.color} rounded-2xl flex items-center justify-center text-white font-bold text-2xl shadow-lg group-hover:shadow-xl transition-shadow`}
                >
                  {item.step}
                </div>

                <div>
                  <h3 className="text-white font-semibold text-xl mb-2">
                    {item.title}
                  </h3>
                  <p className="text-slate-400 leading-relaxed">{item.desc}</p>
                </div>
              </motion.div>
            </FadeIn>
          ))}
        </div>
      </section>

      {/* ==================== CTA ==================== */}
      <section className="max-w-4xl mx-auto px-4 py-24 text-center">
        <FadeIn>
          <motion.div
            whileHover={{ scale: 1.01 }}
            className="relative bg-linear-to-r from-blue-600/20 via-purple-600/20 to-cyan-600/20 border border-blue-500/20 rounded-3xl p-12 md:p-16 overflow-hidden"
          >
            {/* Animated gradient border */}
            <div className="absolute inset-0 rounded-3xl bg-linear-to-r from-blue-500/20 via-purple-500/20 to-cyan-500/20 animate-shimmer opacity-50" />

            <div className="relative z-10">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Ready to Land More Interviews?
              </h2>
              <p className="text-slate-400 mb-8 max-w-xl mx-auto text-lg">
                Most resumes get rejected by ATS before a human ever sees them.
                Fix yours in 30 seconds.
              </p>
              <motion.div
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Link
                  href="/analyze"
                  className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-10 py-4 rounded-xl text-lg font-semibold animate-glow-pulse transition-colors"
                >
                  Analyze Now — It&apos;s Free
                  <ArrowRight className="h-5 w-5" />
                </Link>
              </motion.div>
            </div>
          </motion.div>
        </FadeIn>
      </section>

      {/* ==================== FOOTER ==================== */}
      <footer className="border-t border-slate-800/50 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-slate-500 text-sm">
          <p>
            Built with FastAPI · Next.js · Llama 3.3 70B · sentence-transformers
          </p>
          <p className="mt-1">
            Entirely free and open source. No data stored. No tracking.
          </p>
        </div>
      </footer>
    </div>
  );
}