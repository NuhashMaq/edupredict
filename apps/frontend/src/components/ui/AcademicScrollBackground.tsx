"use client";

import * as React from "react";
import { motion, useScroll, useTransform } from "framer-motion";

import { cn } from "@/lib/cn";

type Props = {
  className?: string;
};

/**
 * AcademicScrollBackground
 * Light, colorful, scroll-reactive background with subtle "academic" cues:
 * - ruled paper lines
 * - floating annotation chips (A+, π, Σ)
 * - soft palette blobs
 *
 * Original implementation.
 */
export function AcademicScrollBackground({ className }: Props) {
  const { scrollY } = useScroll();

  // Subtle parallax: small movement, so it feels “responsive to scroll” without being distracting.
  const blobY1 = useTransform(scrollY, [0, 1200], [0, 80]);
  const blobY2 = useTransform(scrollY, [0, 1200], [0, -60]);
  const chipY = useTransform(scrollY, [0, 1200], [0, 45]);
  const gridY = useTransform(scrollY, [0, 1200], [0, 28]);

  return (
    <div
      aria-hidden
      className={cn(
        "pointer-events-none fixed inset-0 z-0 overflow-hidden",
        className
      )}
    >
      {/* Base wash */}
      <div className="absolute inset-0 bg-[radial-gradient(1200px_650px_at_18%_10%,rgba(20,65,206,0.12),transparent_60%),radial-gradient(1100px_720px_at_84%_18%,rgba(239,127,96,0.16),transparent_60%),radial-gradient(1400px_900px_at_55%_92%,rgba(235,97,95,0.12),transparent_62%)]" />

      {/* Fixed colorful circles (decorative) */}
      <div className="absolute inset-0">
        <div className="absolute left-[3%] top-[14%] h-24 w-24 rounded-full bg-[rgba(20,65,206,0.20)] blur-xl" />
        <div className="absolute left-[10%] top-[72%] h-16 w-16 rounded-full bg-[rgba(235,97,95,0.18)] blur-xl" />
        <div className="absolute left-[42%] top-[8%] h-20 w-20 rounded-full bg-[rgba(239,127,96,0.20)] blur-xl" />
        <div className="absolute left-[62%] top-[22%] h-14 w-14 rounded-full bg-[rgba(20,65,206,0.16)] blur-xl" />
        <div className="absolute left-[76%] top-[58%] h-28 w-28 rounded-full bg-[rgba(239,127,96,0.16)] blur-2xl" />
        <div className="absolute left-[90%] top-[18%] h-16 w-16 rounded-full bg-[rgba(235,97,95,0.16)] blur-xl" />
        <div className="absolute left-[86%] top-[86%] h-20 w-20 rounded-full bg-[rgba(20,65,206,0.12)] blur-2xl" />
        <div className="absolute left-[24%] top-[40%] h-12 w-12 rounded-full bg-[rgba(239,127,96,0.16)] blur-lg" />
        <div className="absolute left-[52%] top-[78%] h-12 w-12 rounded-full bg-[rgba(235,97,95,0.14)] blur-lg" />
      </div>

      {/* Ruled paper lines */}
      <motion.div
        className="absolute inset-0 opacity-[0.35]"
        style={{ y: gridY }}
      >
        <div
          className="absolute inset-0"
          style={{
            backgroundImage:
              "linear-gradient(to bottom, rgba(20,65,206,0.06) 1px, transparent 1px)",
            backgroundSize: "100% 28px"
          }}
        />
        <div
          className="absolute inset-0"
          style={{
            backgroundImage:
              "linear-gradient(to right, rgba(20,65,206,0.05) 1px, transparent 1px)",
            backgroundSize: "120px 100%"
          }}
        />
      </motion.div>

      {/* Soft blobs */}
      <motion.div
        className="absolute -left-40 -top-30 h-[520px] w-[520px] rounded-full blur-3xl"
        style={{ y: blobY1, backgroundColor: "rgba(20,65,206,0.16)" }}
        animate={{ scale: [1, 1.05, 1] }}
        transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute -right-44 top-22.5 h-[520px] w-[520px] rounded-full blur-3xl"
        style={{ y: blobY2, backgroundColor: "rgba(239,127,96,0.18)" }}
        animate={{ scale: [1, 1.06, 1] }}
        transition={{ duration: 11.5, repeat: Infinity, ease: "easeInOut" }}
      />

      {/* Floating academic chips */}
      <motion.div className="absolute inset-0" style={{ y: chipY }}>
        <Chip className="left-[6%] top-[18%]" label="A+" />
        <Chip className="left-[14%] top-[62%]" label="π" />
        <Chip className="left-[78%] top-[28%]" label="Σ" />
        <Chip className="left-[84%] top-[72%]" label="f(x)" />
      </motion.div>

      {/* Vignette to keep content readable */}
      <div className="absolute inset-0 bg-[linear-gradient(to_bottom,rgba(250,222,221,0.65),rgba(250,222,221,0.25),rgba(250,222,221,0.75))]" />
    </div>
  );
}

function Chip({
  className,
  label
}: {
  className: string;
  label: string;
}) {
  return (
    <motion.div
      className={cn(
        "absolute",
        "rounded-full border border-[rgba(20,65,206,0.18)]",
        "bg-white/75 px-3 py-1.5",
        "text-xs font-semibold text-(--edp-blue)",
        "shadow-[0_10px_30px_rgba(20,65,206,0.10)]",
        className
      )}
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: [0, -6, 0] }}
      transition={{ duration: 6.5, repeat: Infinity, ease: "easeInOut" }}
    >
      {label}
    </motion.div>
  );
}
