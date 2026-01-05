"use client";

import * as React from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

import { cn } from "@/lib/cn";

let pluginsRegistered = false;

function ensurePluginsRegistered() {
  if (pluginsRegistered) return;
  gsap.registerPlugin(ScrollTrigger);
  pluginsRegistered = true;
}

type Props = React.HTMLAttributes<HTMLDivElement> & {
  /** Elements matching this selector inside the container are revealed. */
  selector?: string;
  /** Animate on scroll into view (recommended). */
  scroll?: boolean;
  /** Only play once (when scroll=true). */
  once?: boolean;
  /** Stagger between matched elements (seconds). */
  stagger?: number;
  /** Initial Y offset for reveal. */
  y?: number;
  /** Initial scale for reveal. */
  scale?: number;
  /** Duration for each reveal tween. */
  duration?: number;
};

/**
 * Lightweight GSAP reveal wrapper.
 * Usage: add `data-gsap="pop"` to children you want to animate.
 */
export function GsapReveal({
  className,
  children,
  selector = "[data-gsap='pop']",
  scroll = true,
  once = true,
  stagger = 0.08,
  y = 14,
  scale = 0.98,
  duration = 0.55,
  ...props
}: Props) {
  const ref = React.useRef<HTMLDivElement | null>(null);

  React.useLayoutEffect(() => {
    if (typeof window === "undefined") return;

    const reducedMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches;
    if (reducedMotion) return;

    ensurePluginsRegistered();

    const root = ref.current;
    if (!root) return;

    const targets = Array.from(root.querySelectorAll<HTMLElement>(selector));
    if (!targets.length) return;

    const ctx = gsap.context(() => {
      targets.forEach((t, idx) => {
        const delay = idx * stagger;

        if (scroll) {
          gsap.fromTo(
            t,
            { autoAlpha: 0, y, scale },
            {
              autoAlpha: 1,
              y: 0,
              scale: 1,
              delay,
              duration,
              ease: "power3.out",
              clearProps: "transform,opacity",
              scrollTrigger: {
                trigger: t,
                start: "top 88%",
                once
              }
            }
          );
          return;
        }

        gsap.fromTo(
          t,
          { autoAlpha: 0, y, scale },
          {
            autoAlpha: 1,
            y: 0,
            scale: 1,
            delay,
            duration,
            ease: "power3.out",
            clearProps: "transform,opacity"
          }
        );
      });
    }, root);

    return () => {
      ctx.revert();
    };
  }, [selector, scroll, once, stagger, y, scale, duration]);

  return (
    <div ref={ref} className={cn(className)} {...props}>
      {children}
    </div>
  );
}
