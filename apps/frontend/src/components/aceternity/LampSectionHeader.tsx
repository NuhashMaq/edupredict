"use client";

import * as React from "react";

import { cn } from "@/lib/cn";

type Props = {
  className?: string;
  eyebrow?: string;
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  children?: React.ReactNode;
  align?: "left" | "center";
  /** Show the bottom divider + accent pill. Defaults to true. */
  showDivider?: boolean;
};

/**
 * Lamp Section Header (Aceternity-inspired).
 * Now: clean, light section header surface (lamp effect removed).
 */
export function LampSectionHeader({
  className,
  eyebrow,
  title,
  subtitle,
  children,
  align = "center",
  showDivider = true
}: Props) {
  const isLeft = align === "left";

  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-3xl border border-[rgba(20,65,206,0.14)] bg-white/75 text-slate-900",
        className
      )}
    >
      {/* Subtle surface wash (no lamp beams) */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(900px_360px_at_18%_12%,rgba(20,65,206,0.10),transparent_60%),radial-gradient(900px_360px_at_82%_18%,rgba(239,127,96,0.12),transparent_62%)]"
      />

      {/* Content */}
      <div
        className={cn(
          "relative z-10",
          "px-6 py-10 sm:px-10 sm:py-14",
          isLeft ? "text-left" : "text-center",
          isLeft ? "mx-0" : "mx-auto"
        )}
      >
        {eyebrow ? (
          <div className="text-xs font-semibold tracking-[0.22em] text-slate-600">{eyebrow}</div>
        ) : null}

        <div
          className={cn(
            "mt-4 text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl lg:text-6xl",
            "text-balance"
          )}
        >
          {title}
        </div>

        {subtitle ? (
          <div className={cn("mt-4 text-base leading-7 text-slate-600 sm:text-lg")}>{subtitle}</div>
        ) : null}

        {children ? (
          <div className={cn("mt-6", isLeft ? "mr-auto" : "mx-auto")}>{children}</div>
        ) : null}

        {showDivider ? (
          <>
            <div aria-hidden className={cn("mt-8 h-px w-full", "bg-linear-to-r from-transparent via-[rgba(20,65,206,0.16)] to-transparent")} />

            <div aria-hidden className={cn("mx-auto mt-3 h-1 w-24 rounded-full", isLeft ? "ml-0" : "", "bg-[linear-gradient(90deg,rgba(20,65,206,0.65),rgba(239,127,96,0.55),rgba(235,97,95,0.55))]")} />
          </>
        ) : null}
      </div>
    </div>
  );
}
