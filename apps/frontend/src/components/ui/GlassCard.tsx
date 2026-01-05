import * as React from "react";

import { cn } from "@/lib/cn";

type Props = React.HTMLAttributes<HTMLDivElement> & {
  tone?: "default" | "emerald" | "cyan" | "fuchsia";
  /** Back-compat only (lamp effect removed). */
  lamp?: boolean;
  /**
   * Enables the hover lift + shadow interaction.
   * Per UI requirements this should only be used on the homepage.
   */
  interactive?: boolean;
};

export function GlassCard({ className, tone = "default", lamp, interactive = false, children, ...props }: Props) {
  void lamp;
  const toneClasses =
    tone === "emerald"
      ? "before:from-[rgba(20,65,206,0.10)] before:via-[rgba(239,127,96,0.12)]"
      : tone === "cyan"
        ? "before:from-[rgba(20,65,206,0.12)] before:via-[rgba(235,97,95,0.10)]"
        : tone === "fuchsia"
          ? "before:from-[rgba(235,97,95,0.12)] before:via-[rgba(20,65,206,0.10)]"
          : "before:from-[rgba(20,65,206,0.10)] before:via-[rgba(239,127,96,0.10)]";

  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-3xl text-slate-900 backdrop-blur-xl",
        "text-base leading-relaxed",
        "bg-[linear-gradient(135deg,rgba(255,255,255,0.86),rgba(250,222,221,0.58))]",
        "border border-[rgba(20,65,206,0.10)] ring-1 ring-[rgba(20,65,206,0.10)]",
        interactive
          ? "shadow-[0_18px_70px_rgba(20,65,206,0.16),0_14px_52px_rgba(239,127,96,0.12),0_10px_36px_rgba(235,97,95,0.10)] transition will-change-transform hover:-translate-y-1 hover:shadow-[0_22px_90px_rgba(20,65,206,0.18),0_18px_70px_rgba(239,127,96,0.14),0_14px_52px_rgba(235,97,95,0.12)] hover:ring-[rgba(20,65,206,0.18)]"
          : "shadow-none",
        "before:pointer-events-none before:absolute before:inset-0 before:bg-linear-to-br before:to-transparent",
        "before:opacity-100",
        toneClasses,
        className
      )}
      {...props}
    >
      <div className="relative z-10">{children}</div>
    </div>
  );
}
