"use client";

import * as React from "react";
import { AnimatePresence, motion } from "framer-motion";

import { cn } from "@/lib/cn";

type Props = {
  className?: string;
  visible: boolean;
  steps: string[];
  /** 0-based index of active step. */
  activeIndex?: number;
};

/**
 * Multi Step Loader (Aceternity-inspired).
 * A small overlay loader for operations that take time.
 */
export function MultiStepLoader({ className, visible, steps, activeIndex = 0 }: Props) {
  const safeIndex = Math.min(Math.max(activeIndex, 0), Math.max(steps.length - 1, 0));

  return (
    <AnimatePresence>
      {visible ? (
        <motion.div
          aria-live="polite"
          className={cn(
            "fixed inset-0 z-70 flex items-center justify-center",
            "bg-[rgba(250,222,221,0.82)] backdrop-blur-sm",
            className
          )}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <motion.div
            className={cn(
              "w-full max-w-md rounded-2xl border border-[rgba(20,65,206,0.14)] bg-white/80 p-6",
              "shadow-[0_0_0_1px_rgba(20,65,206,0.06),0_30px_120px_rgba(20,65,206,0.14)]"
            )}
            initial={{ y: 10, scale: 0.98, opacity: 0 }}
            animate={{ y: 0, scale: 1, opacity: 1 }}
            exit={{ y: 10, scale: 0.98, opacity: 0 }}
            transition={{ duration: 0.18, ease: "easeOut" }}
          >
            <div className="flex items-center justify-between gap-3">
              <div className="text-base font-semibold text-slate-900">Working…</div>
              <div className="h-2 w-2 animate-pulse rounded-full bg-[#1441CE]" />
            </div>

            <div className="mt-4 grid gap-2">
              {steps.map((s, i) => {
                const active = i === safeIndex;
                const done = i < safeIndex;
                return (
                  <div
                    key={`${i}-${s}`}
                    className={cn(
                      "flex items-center gap-3 rounded-xl border px-3 py-2",
                      done
                        ? "border-[rgba(20,65,206,0.18)] bg-[rgba(20,65,206,0.06)]"
                        : active
                          ? "border-[rgba(239,127,96,0.22)] bg-[rgba(239,127,96,0.08)]"
                          : "border-[rgba(20,65,206,0.14)] bg-white/55"
                    )}
                  >
                    <div
                      className={cn(
                        "h-2.5 w-2.5 rounded-full",
                        done
                          ? "bg-[#1441CE]"
                          : active
                            ? "bg-[#EF7F60]"
                            : "bg-[rgba(20,65,206,0.22)]"
                      )}
                    />
                    <div
                      className={cn(
                        "text-base",
                        done ? "text-slate-700" : active ? "text-slate-900" : "text-slate-600"
                      )}
                    >
                      {s}
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}
