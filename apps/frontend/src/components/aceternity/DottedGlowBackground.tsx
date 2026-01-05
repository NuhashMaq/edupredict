"use client";

import * as React from "react";
import { motion } from "framer-motion";

import { cn } from "@/lib/cn";

type Props = {
  className?: string;
  /** Dot color (CSS color). Default is cyan-ish. */
  dotColor?: string;
  /** Dot spacing in px. Default 22. */
  dotSize?: number;
};

/**
 * Dotted Glow Background (Aceternity-inspired).
 * Purely decorative: animated dot opacity + soft glows.
 */
export function DottedGlowBackground({
  className,
  dotColor = "rgba(20,65,206,0.18)",
  dotSize = 22
}: Props) {
  return (
    <div
      aria-hidden
      className={cn("pointer-events-none absolute inset-0 overflow-hidden", className)}
    >
      {/* Dot field */}
      <motion.div
        className="absolute inset-0"
        style={{
          backgroundImage: `radial-gradient(${dotColor} 1px, transparent 1px)`,
          backgroundSize: `${dotSize}px ${dotSize}px`
        }}
        initial={{ opacity: 0.22 }}
        animate={{ opacity: [0.16, 0.34, 0.16] }}
        transition={{ duration: 7.5, repeat: Infinity, ease: "easeInOut" }}
      />

      {/* Soft glows */}
      <div className="absolute inset-0 bg-[radial-gradient(900px_520px_at_18%_12%,rgba(20,65,206,0.16),transparent_60%),radial-gradient(820px_520px_at_84%_18%,rgba(239,127,96,0.14),transparent_60%),radial-gradient(980px_640px_at_55%_92%,rgba(235,97,95,0.12),transparent_62%)]" />
    </div>
  );
}
