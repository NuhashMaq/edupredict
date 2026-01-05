"use client";

import * as React from "react";
import Image from "next/image";
import { AnimatePresence, motion } from "framer-motion";

import { cn } from "@/lib/cn";

export type ImageSlide = {
  title: string;
  subtitle?: string;
  /** Tailwind class to paint the slide background (use a solid class like "bg-black" when using photos). */
  backgroundClassName: string;
  /** Optional background image (local or remote). */
  imageSrc?: string;
  imageAlt?: string;
};

type Props = {
  className?: string;
  slides: ImageSlide[];
};

/**
 * Images Slider (Aceternity-inspired).
 * Keyboard accessible (←/→), animated transitions.
 * Supports optional /public images as slide backgrounds.
 */
export function ImageSlider({ className, slides }: Props) {
  const [index, setIndex] = React.useState(0);

  const safeSlides = slides.length ? slides : [];
  const active = safeSlides[index];

  const go = React.useCallback(
    (dir: -1 | 1) => {
      if (!safeSlides.length) return;
      setIndex((i) => {
        const next = (i + dir + safeSlides.length) % safeSlides.length;
        return next;
      });
    },
    [safeSlides.length]
  );

  React.useEffect(() => {
    if (!safeSlides.length) return;

    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "ArrowLeft") go(-1);
      if (e.key === "ArrowRight") go(1);
    };

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [go, safeSlides.length]);

  if (!active) return null;

  const isSvg = typeof active.imageSrc === "string" && /\.svg($|\?)/i.test(active.imageSrc);

  return (
    <div className={cn("grid gap-3", className)}>
      <div className="flex items-center justify-between gap-3">
        <div className="text-base font-semibold text-slate-900">Preview</div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => go(-1)}
            className="text-lg sm:text-xl font-semibold text-(--edp-orange) underline-offset-4 hover:underline"
          >
            Prev
          </button>
          <button
            type="button"
            onClick={() => go(1)}
            className="text-lg sm:text-xl font-semibold text-(--edp-blue) underline-offset-4 hover:underline"
          >
            Next
          </button>
        </div>
      </div>
      <div className="relative overflow-hidden rounded-2xl bg-[linear-gradient(135deg,rgba(255,255,255,0.86),rgba(250,222,221,0.58))] shadow-[0_18px_70px_rgba(20,65,206,0.14),0_14px_52px_rgba(239,127,96,0.12)]">
        <AnimatePresence mode="wait">
          <motion.div
            key={index}
            className={cn(
              "relative h-96 w-full sm:h-110 lg:h-120",
              "flex items-end",
              active.backgroundClassName
            )}
            initial={{ opacity: 0, x: 18 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -18 }}
            transition={{ duration: 0.22, ease: "easeOut" }}
          >
            {active.imageSrc ? (
              <Image
                src={active.imageSrc}
                alt={active.imageAlt ?? active.title}
                fill
                priority={index === 0}
                unoptimized={/^https?:\/\//.test(active.imageSrc)}
                sizes="(min-width: 1024px) 960px, 100vw"
                className={cn(
                  isSvg ? "object-contain p-6" : "object-cover"
                )}
              />
            ) : null}

            {/* Simple readability overlay (no patterns) */}
            <div
              aria-hidden
              className="pointer-events-none absolute inset-0 bg-linear-to-t from-[rgba(250,222,221,0.88)] via-[rgba(255,255,255,0.25)] to-transparent"
            />

            <div className="relative w-full p-5">
              <div className="text-xl font-semibold text-slate-900">{active.title}</div>
              {active.subtitle ? (
                <div className="mt-1 text-base text-slate-700">{active.subtitle}</div>
              ) : null}
            </div>
          </motion.div>
        </AnimatePresence>
      </div>

      <div className="flex items-center gap-2">
        {safeSlides.map((_, i) => (
          <button
            key={i}
            type="button"
            onClick={() => setIndex(i)}
            aria-label={`Go to slide ${i + 1}`}
            className={cn(
              "h-2.5 w-2.5 rounded-full border",
              i === index
                ? "border-(--edp-blue) bg-(--edp-blue) shadow-[0_0_0_4px_rgba(20,65,206,0.14)]"
                : "border-[rgba(20,65,206,0.22)] bg-white/70 hover:bg-[rgba(250,222,221,0.80)]"
            )}
          />
        ))}
      </div>
    </div>
  );
}
