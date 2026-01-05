import Link from "next/link";
import type { ComponentProps } from "react";

import { cn } from "@/lib/cn";

type Props = {
  className?: string;
  href?: ComponentProps<typeof Link>["href"];
};

export function BrandLogo({ className, href = "/" }: Props) {
  return (
    <Link
      href={href}
      className={cn(
        // Keep the logo identical everywhere.
        "text-4xl sm:text-5xl font-black tracking-tight leading-none text-slate-900",
        className
      )}
    >
      <span
        className={
          "font-black tracking-tight leading-none " +
          "[font-family:var(--font-logo),var(--font-space),ui-sans-serif,system-ui]"
        }
      >
        <span className="text-(--edp-blue)">edu</span>
        <span className="text-(--edp-orange)">predict</span>
      </span>
    </Link>
  );
}
