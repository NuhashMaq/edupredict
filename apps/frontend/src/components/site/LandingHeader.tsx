"use client";

import * as React from "react";
import Link from "next/link";

import { HoverBorderGradient } from "@/components/aceternity";
import { BrandLogo } from "@/components/site/BrandLogo";
import { cn } from "@/lib/cn";

type Props = {
  className?: string;
};

export function LandingHeader({ className }: Props) {
  const [open, setOpen] = React.useState(false);

  const primaryCtaClassName = "h-12 px-7 text-lg font-semibold";
  const primaryCtaRounded = "rounded-full";

  React.useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false);
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  return (
    <div className={cn("sticky top-0 z-50 border-b border-[rgba(20,65,206,0.14)] bg-white/75 backdrop-blur-xl", className)}>
      <div className="mx-auto flex w-full max-w-screen-2xl items-center justify-between gap-3 px-3 py-6 sm:px-6">
        <div onClick={() => setOpen(false)}>
          <BrandLogo />
        </div>

        {/* Desktop nav */}
        <nav className="hidden items-center gap-3 sm:flex">
          <Link href="/login" className="block">
            <HoverBorderGradient
              interactive
              className={
                "h-12 px-7 text-lg font-semibold bg-[rgba(239,127,96,0.95)] text-white " +
                "border-[rgba(239,127,96,0.25)] ring-1 ring-[rgba(239,127,96,0.20)] " +
                "hover:shadow-[0_0_0_1px_rgba(239,127,96,0.25),0_18px_70px_rgba(239,127,96,0.26),0_14px_52px_rgba(235,97,95,0.18)]"
              }
              roundedClassName={primaryCtaRounded}
            >
              Sign in
            </HoverBorderGradient>
          </Link>
          <Link href="/register" className="block">
            <HoverBorderGradient
              interactive
              className={primaryCtaClassName}
              roundedClassName={primaryCtaRounded}
            >
              Sign up
            </HoverBorderGradient>
          </Link>
        </nav>

        {/* Mobile menu button */}
        <div className="flex items-center gap-2 sm:hidden">
          <button
            type="button"
            className="inline-flex h-11 w-11 items-center justify-center rounded-xl border border-[rgba(20,65,206,0.14)] bg-white/70 text-slate-900 shadow-[0_10px_30px_rgba(20,65,206,0.10)]"
            aria-label={open ? "Close menu" : "Open menu"}
            aria-expanded={open}
            onClick={() => setOpen((v) => !v)}
          >
            <span className="sr-only">Menu</span>
            <span className="relative block h-4 w-5">
              <span
                className={cn(
                  "absolute left-0 top-0 h-0.5 w-5 rounded-full bg-slate-900 transition-transform",
                  open ? "translate-y-1.75 rotate-45" : ""
                )}
              />
              <span
                className={cn(
                  "absolute left-0 top-1.75 h-0.5 w-5 rounded-full bg-slate-900 transition-opacity",
                  open ? "opacity-0" : "opacity-100"
                )}
              />
              <span
                className={cn(
                  "absolute left-0 top-3.5 h-0.5 w-5 rounded-full bg-slate-900 transition-transform",
                  open ? "-translate-y-1.75 -rotate-45" : ""
                )}
              />
            </span>
          </button>
        </div>
      </div>

      {/* Mobile menu panel */}
      {open ? (
        <div className="sm:hidden">
          <div className="mx-auto grid max-w-screen-2xl gap-2 px-3 pb-6 sm:px-6">
            <a
              href="#features"
              className="rounded-xl border border-[rgba(20,65,206,0.14)] bg-white/70 px-4 py-3 text-base font-semibold text-slate-800"
              onClick={() => setOpen(false)}
            >
              Features
            </a>
            <a
              href="#showcase"
              className="rounded-xl border border-[rgba(20,65,206,0.14)] bg-white/70 px-4 py-3 text-base font-semibold text-slate-800"
              onClick={() => setOpen(false)}
            >
              Showcase
            </a>
            <a
              href="#get-started"
              className="rounded-xl border border-[rgba(20,65,206,0.14)] bg-white/70 px-4 py-3 text-base font-semibold text-slate-800"
              onClick={() => setOpen(false)}
            >
              Get started
            </a>

            <div className="grid grid-cols-2 gap-2 pt-1">
              <Link href="/login" className="block" onClick={() => setOpen(false)}>
                <HoverBorderGradient
                  interactive
                  className={
                    "w-full h-12 px-7 text-lg font-semibold bg-[rgba(239,127,96,0.95)] text-white " +
                    "border-[rgba(239,127,96,0.25)] ring-1 ring-[rgba(239,127,96,0.20)] " +
                    "hover:shadow-[0_0_0_1px_rgba(239,127,96,0.25),0_18px_70px_rgba(239,127,96,0.26),0_14px_52px_rgba(235,97,95,0.18)]"
                  }
                  roundedClassName={primaryCtaRounded}
                >
                  Sign in
                </HoverBorderGradient>
              </Link>
              <Link href="/register" className="block" onClick={() => setOpen(false)}>
                <HoverBorderGradient
                  interactive
                  className={"w-full " + primaryCtaClassName}
                  roundedClassName={primaryCtaRounded}
                >
                  Sign up
                </HoverBorderGradient>
              </Link>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
