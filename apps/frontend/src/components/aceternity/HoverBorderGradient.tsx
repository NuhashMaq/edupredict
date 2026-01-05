"use client";

import * as React from "react";
import { motion, useMotionTemplate, useMotionValue } from "framer-motion";

import { cn } from "@/lib/cn";

type Props = {
  className?: string;
  children: React.ReactNode;
  type?: "button" | "submit" | "reset";
  disabled?: boolean;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
  roundedClassName?: string;
  variant?: "blue" | "orange";
  /**
   * Enables the animated hover/glow interaction.
   * Keep this true only on the homepage per UI requirements.
   */
  interactive?: boolean;
};

/**
 * Aceternity-inspired hover border gradient button.
 * Original implementation (no copied source).
 */
export function HoverBorderGradient({
  className,
  children,
  type,
  disabled,
  onClick,
  roundedClassName,
  variant = "blue",
  interactive = true
}: Props) {
  const mx = useMotionValue(0);
  const my = useMotionValue(0);

  const styles =
    variant === "orange"
      ? {
          base: "bg-(--edp-orange) text-white",
          border: "border border-[rgba(239,127,96,0.20)]",
          ring: "ring-1 ring-[rgba(239,127,96,0.24)]",
          shadow:
            "hover:shadow-[0_0_0_1px_rgba(239,127,96,0.22),0_22px_85px_rgba(239,127,96,0.20),0_18px_70px_rgba(20,65,206,0.18),0_14px_54px_rgba(235,97,95,0.14)]",
          glow: "rgba(20,65,206,0.24), rgba(235,97,95,0.22), rgba(239,127,96,0.26)"
        }
      : {
          base: "bg-(--edp-blue) text-white",
          border: "border border-[rgba(20,65,206,0.18)]",
          ring: "ring-1 ring-[rgba(20,65,206,0.22)]",
          shadow:
            "hover:shadow-[0_0_0_1px_rgba(20,65,206,0.24),0_22px_85px_rgba(20,65,206,0.22),0_18px_70px_rgba(239,127,96,0.20),0_14px_54px_rgba(235,97,95,0.16)]",
          glow: "rgba(239,127,96,0.28), rgba(235,97,95,0.22), rgba(20,65,206,0.22)"
        };

  const background = useMotionTemplate`radial-gradient(280px 160px at ${mx}px ${my}px, ${styles.glow}, transparent 72%)`;

  return (
    <motion.button
      type={type ?? "button"}
      disabled={disabled}
      onClick={onClick}
      whileHover={interactive && !disabled ? { scale: 1.03, y: -1.5 } : undefined}
      whileTap={interactive && !disabled ? { scale: 0.99, y: 0 } : undefined}
      onPointerMove={
        interactive
          ? (e) => {
              const el = e.currentTarget;
              const rect = el.getBoundingClientRect();
              mx.set(e.clientX - rect.left);
              my.set(e.clientY - rect.top);
            }
          : undefined
      }
      className={cn(
        "relative inline-flex h-12 items-center justify-center whitespace-nowrap px-7 text-xl! font-semibold leading-none",
        roundedClassName ?? "rounded-full",
        styles.base,
        styles.border,
        styles.ring,
        "transition-shadow",
        interactive ? styles.shadow : null,
        "disabled:cursor-not-allowed disabled:opacity-60",
        className
      )}
    >
      {interactive ? (
        <motion.span
          aria-hidden
          className={cn("absolute inset-0", roundedClassName ?? "rounded-full")}
          style={{ background }}
        />
      ) : null}
      <span className="relative z-10">{children}</span>
    </motion.button>
  );
}
