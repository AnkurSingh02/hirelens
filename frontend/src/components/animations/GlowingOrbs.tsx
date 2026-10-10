"use client";

export default function GlowingOrbs() {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {/* Orb 1 — Blue, top left */}
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-orb-1" />

      {/* Orb 2 — Purple, top right */}
      <div className="absolute -top-20 -right-20 w-80 h-80 bg-purple-500/15 rounded-full blur-3xl animate-orb-2" />

      {/* Orb 3 — Cyan, bottom center */}
      <div className="absolute -bottom-40 left-1/3 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl animate-orb-3" />

      {/* Orb 4 — Blue, middle right */}
      <div className="absolute top-1/2 -right-20 w-64 h-64 bg-blue-600/10 rounded-full blur-3xl animate-orb-4" />

      {/* Subtle grid overlay */}
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `
            linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)
          `,
          backgroundSize: "60px 60px",
        }}
      />
    </div>
  );
}