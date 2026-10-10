"use client";

import { motion } from "framer-motion";
import { FileSearch } from "lucide-react";
import Link from "next/link";

export default function Navbar() {
  return (
    <motion.nav
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="border-b border-slate-800/50 bg-slate-950/60 backdrop-blur-xl sticky top-0 z-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <motion.div
              whileHover={{ rotate: 15, scale: 1.1 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <FileSearch className="h-8 w-8 text-blue-500" />
            </motion.div>
            <span className="text-xl font-bold text-white">
              Hire<span className="text-blue-500">Lens</span>
            </span>
          </Link>

          {/* Nav links */}
          <div className="flex items-center gap-6">
            <motion.div whileHover={{ y: -2 }}>
              <Link
                href="/"
                className="text-slate-400 hover:text-white transition-colors"
              >
                Home
              </Link>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Link
                href="/analyze"
                className="relative bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg transition-colors font-medium overflow-hidden group"
              >
                {/* Shimmer effect on hover */}
                <span className="relative z-10">Analyze Resume</span>
                <div className="absolute inset-0 bg-linear-to-r from-transparent via-white/20 to-transparent translate-x-[-200%] group-hover:translate-x-[200%] transition-transform duration-700" />
              </Link>
            </motion.div>
          </div>
        </div>
      </div>
    </motion.nav>
  );
}