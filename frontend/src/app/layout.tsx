import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import GlowingOrbs from "@/components/animations/GlowingOrbs";
import CursorGlow from "@/components/animations/CursorGlow";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "HireLens — AI Resume Screener & ATS Optimizer",
  description:
    "Upload your resume, paste a job description, get instant AI-powered analysis.",
  icons: {
    icon: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔍</text></svg>",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${inter.className} bg-slate-950 text-white min-h-screen overflow-x-hidden`}
      >
        {/* Animated background — always visible */}
        <GlowingOrbs />

        {/* Cursor glow — desktop only */}
        <CursorGlow />

        {/* Content sits above the orbs */}
        <div className="relative z-10">
          <Navbar />
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}