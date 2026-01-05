"use client";

import * as React from "react";
import { motion, useInView } from "framer-motion";

import { cn } from "@/lib/cn";

type Direction = "left" | "right" | "up" | "down";

type Props = {
  children: React.ReactNode;
  className?: string;
  delay?: number; // seconds
  distance?: number; // px
  seed?: string | number; // stable seed for deterministic direction
  direction?: Direction; // force direction if desired
  /**
   * When true, the reveal may come from left/right as well as up/down.
   * Defaults to false to avoid column overlap on desktop layouts.
   */
  allowHorizontal?: boolean;
};

const vectors = {
  left: { x: -1, y: 0 },
  right: { x: 1, y: 0 },
  up: { x: 0, y: -1 },
  down: { x: 0, y: 1 }
} as const;

const orderVertical: Direction[] = ["up", "down"];
const orderAll: Direction[] = ["left", "right", "up", "down"];

function hashToIndex(input: string, modulo: number) {
  let h = 0;
  for (let i = 0; i < input.length; i++) h = (h * 31 + input.charCodeAt(i)) | 0;
  return Math.abs(h) % modulo;
}

/**
 * Deterministic "random side" reveal (SSR/CSR stable).
 * Uses in-view to trigger animation. Hidden styles use strings to avoid hydration diffs.
 */
export function RandomReveal({
  children,
  className,
  delay = 0,
  distance = 28,
  seed,
  direction,
  allowHorizontal = false
}: Props) {
  const reactId = React.useId();
  const ref = React.useRef<HTMLDivElement | null>(null);
  const inView = useInView(ref, { once: true, amount: 0.2 });

  const chosen = React.useMemo<Direction>(() => {
    if (direction) return direction;
    const key = `${seed ?? ""}:${reactId}`;
    const pool = allowHorizontal ? orderAll : orderVertical;
    return pool[hashToIndex(key, pool.length)];
  }, [direction, seed, reactId, allowHorizontal]);

  const dir = vectors[chosen];
  const dx = dir.x * distance;
  const dy = dir.y * distance;

  // Use strings so SSR HTML attribute values match what client expects.
  const hidden = React.useMemo(
    () => ({
      opacity: "0",
      transform: `translate3d(${dx}px, ${dy}px, 0)`
    }),
    [dx, dy]
  );

  const shown = React.useMemo(
    () => ({
      opacity: 1,
      transform: "translate3d(0px, 0px, 0)"
    }),
    []
  );

  return (
    <motion.div
      ref={ref}
      className={cn(className)}
      initial={false}
      style={hidden}
      animate={inView ? shown : hidden}
      transition={{ duration: 0.65, ease: [0.22, 1, 0.36, 1], delay }}
    >
      {children}
    </motion.div>
  );
}