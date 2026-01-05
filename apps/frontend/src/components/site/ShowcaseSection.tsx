"use client";

import * as React from "react";
import { AnimatePresence, motion } from "framer-motion";

import { ImageSlider } from "@/components/aceternity";
import type { ImageSlide } from "@/components/aceternity/ImageSlider";

type Props = {
  productSlides: ImageSlide[];
  conceptSlides: ImageSlide[];
};

export function ShowcaseSection({ productSlides, conceptSlides }: Props) {
  const [mode, setMode] = React.useState<"product" | "concept">("product");
  const isConcept = mode === "concept";
  const activeSlides = isConcept ? conceptSlides : productSlides;

  return (
    <section id="showcase" className="mt-14 scroll-mt-24">
      <section className="rounded-3xl border border-[rgba(20,65,206,0.14)] bg-white/70 p-5 sm:p-7">
        <div className="grid justify-items-center gap-4 text-center">
          <div className="text-xs font-semibold tracking-[0.22em] text-slate-600">SHOWCASE</div>
          <div className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">A quick tour</div>
          <div className="max-w-2xl text-sm text-slate-600 sm:text-base">
            See how the experience scales from overview to details.
          </div>

          <div className="mt-1 flex items-center justify-center gap-2">
            <button
              type="button"
              onClick={() => setMode("product")}
              className={
                "rounded-2xl px-4 py-2 text-base font-semibold transition " +
                (mode === "product"
                  ? "bg-(--edp-blue) text-white shadow-[0_16px_44px_rgba(20,65,206,0.24)]"
                  : "border border-[rgba(20,65,206,0.14)] bg-white/70 text-slate-700 hover:bg-white")
              }
              aria-pressed={mode === "product"}
            >
              Product
            </button>
            <button
              type="button"
              onClick={() => setMode("concept")}
              className={
                "rounded-2xl px-4 py-2 text-base font-semibold transition " +
                (mode === "concept"
                  ? "bg-(--edp-orange) text-white shadow-[0_16px_44px_rgba(239,127,96,0.26)]"
                  : "border border-[rgba(20,65,206,0.14)] bg-white/70 text-slate-700 hover:bg-white")
              }
              aria-pressed={mode === "concept"}
            >
              Concept
            </button>
          </div>

          <div className="mt-1">
            <div className="text-base font-semibold text-slate-900">
              {isConcept ? "Concept tour" : "Product tour"}
            </div>
            <div className="mt-1 text-sm text-slate-600">
              {isConcept
                ? "A lightweight walkthrough of how EduPredict turns records into explainable decisions."
                : "Preview the key screens and workflows."}
            </div>
          </div>
        </div>

        <div className="mt-5">
          <AnimatePresence mode="wait">
            <motion.div
              key={mode}
              initial={{ opacity: 0, x: 22 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -22 }}
              transition={{ duration: 0.22, ease: "easeOut" }}
            >
              <ImageSlider slides={activeSlides} />
            </motion.div>
          </AnimatePresence>
        </div>
      </section>
    </section>
  );
}
