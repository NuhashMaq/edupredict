"use client";

import { motion } from "framer-motion";

import { cn } from "@/lib/cn";

type Props = {
  className?: string;
};

/**
 * Decorative motion-only background for the landing page.
 * Kept as a client component so the server-rendered landing page stays prerender-safe.
 */
export function LandingMotionBackground({ className }: Props) {
  return (
    <div aria-hidden className={cn("pointer-events-none absolute inset-0", className)}>
      <motion.div
        className="absolute -left-24 top-24 h-72 w-72 rounded-full bg-[rgba(20,65,206,0.14)] blur-3xl"
        animate={{ x: [0, 36, -10, 0], y: [0, -22, 14, 0], scale: [1, 1.08, 1.02, 1] }}
        transition={{ duration: 16, ease: "easeInOut", repeat: Infinity }}
      />
      <motion.div
        className="absolute -right-35 top-52 h-105 w-105 rounded-full bg-[rgba(239,127,96,0.16)] blur-3xl"
        animate={{ x: [0, -26, 12, 0], y: [0, 18, -10, 0], scale: [1, 1.06, 1.01, 1] }}
        transition={{ duration: 18, ease: "easeInOut", repeat: Infinity }}
      />
      <motion.div
        className="absolute left-[38%] top-[72%] h-[520px] w-[520px] rounded-full bg-[rgba(235,97,95,0.12)] blur-3xl"
        animate={{ x: [0, 20, -18, 0], y: [0, 10, -16, 0] }}
        transition={{ duration: 22, ease: "easeInOut", repeat: Infinity }}
      />

      <motion.div
        className="absolute left-[-15%] top-[35%] h-px w-[70%] rotate-[-10deg] bg-linear-to-r from-transparent via-[rgba(20,65,206,0.20)] to-transparent"
        animate={{ x: [0, 90, 0] }}
        transition={{ duration: 14, ease: "easeInOut", repeat: Infinity }}
      />
      <motion.div
        className="absolute right-[-10%] top-[18%] h-px w-[62%] rotate-12 bg-linear-to-r from-transparent via-[rgba(239,127,96,0.22)] to-transparent"
        animate={{ x: [0, -80, 0] }}
        transition={{ duration: 17, ease: "easeInOut", repeat: Infinity }}
      />
    </div>
  );
}
