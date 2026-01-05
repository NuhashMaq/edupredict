"use client";

import * as React from "react";

import { cn } from "@/lib/cn";

type Props = React.HTMLAttributes<HTMLDivElement> & {
  /** Kept for backward compatibility; no longer used for a gradient spotlight effect. */
  radius?: number;
  /** Back-compat only (lamp effect removed). */
  lamp?: boolean;
  /** Disable hover lift/glow effects (useful for continuously-animated cards). */
  interactive?: boolean;
};

/**
 * Card Spotlight (Aceternity-inspired).
 * Simplified to a clean card surface (no gradient/pattern effects).
 */
export function CardSpotlight({ className, children, radius: _radius, lamp, ...props }: Props) {
  void _radius;
  void lamp;
  const interactive = props.interactive ?? true;

  // Remove custom prop before spreading to DOM.
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { interactive: _interactive, ...rest } = props;
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-2xl bg-[linear-gradient(135deg,rgba(255,255,255,0.86),rgba(250,222,221,0.58))] text-slate-900",
        "border border-[rgba(20,65,206,0.12)] ring-1 ring-[rgba(20,65,206,0.10)]",
        "shadow-[0_16px_60px_rgba(20,65,206,0.14),0_10px_36px_rgba(239,127,96,0.10),0_10px_28px_rgba(235,97,95,0.08)]",
        "transition will-change-transform",
        interactive
          ? "hover:-translate-y-1 hover:shadow-[0_22px_90px_rgba(20,65,206,0.16),0_18px_70px_rgba(239,127,96,0.12),0_14px_52px_rgba(235,97,95,0.10)] hover:ring-[rgba(20,65,206,0.16)]"
          : "",
        className
      )}
      {...rest}
    >
      <div className="relative z-10">{children}</div>
    </div>
  );
}
