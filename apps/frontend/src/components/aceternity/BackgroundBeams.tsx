"use client";

import * as React from "react";
import { motion } from "framer-motion";

import { cn } from "@/lib/cn";

/**
 * Aceternity-inspired animated beams background.
 * Original implementation (no copied source).
 */
export function BackgroundBeams({ className }: { className?: string }) {
  const beams = React.useMemo(
    () =>
      Array.from({ length: 10 }).map((_, i) => ({
        id: i,
        left: `${Math.round((i / 10) * 100)}%`,
        delay: i * 0.15,
        duration: 4.5 + (i % 3) * 1.2
      })),
    []
  );

  return (
    <div
      aria-hidden
      className={cn(
        "pointer-events-none absolute inset-0 overflow-hidden",
        className
      )}
    >
      <div className="absolute inset-0 bg-[radial-gradient(1000px_520px_at_18%_0%,rgba(20,65,206,0.14),transparent_62%),radial-gradient(900px_620px_at_82%_10%,rgba(239,127,96,0.14),transparent_62%),radial-gradient(1100px_760px_at_50%_100%,rgba(235,97,95,0.10),transparent_62%)]" />

      {beams.map((b) => (
        <motion.div
          key={b.id}
          className="absolute -top-[30%] h-[160%] w-px bg-linear-to-b from-transparent via-[rgba(20,65,206,0.18)] to-transparent"
          style={{ left: b.left }}
          initial={{ opacity: 0.2, y: -40 }}
          animate={{ opacity: [0.15, 0.42, 0.15], y: [0, 60, 0] }}
          transition={{
            duration: b.duration,
            delay: b.delay,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
      ))}

      <div className="absolute inset-0 bg-linear-to-t from-[rgba(250,222,221,0.85)] via-[rgba(250,222,221,0.18)] to-[rgba(255,255,255,0.45)]" />
    </div>
  );
}
