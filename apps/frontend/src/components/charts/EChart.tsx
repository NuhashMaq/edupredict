"use client";

import * as React from "react";

export type EChartOption = import("echarts").EChartsOption;

export function EChart({
  option,
  className
}: {
  option: EChartOption;
  className?: string;
}) {
  const ref = React.useRef<HTMLDivElement | null>(null);

  React.useEffect(() => {
    let chart: import("echarts").EChartsType | null = null;
    let alive = true;

    (async () => {
      const echarts = await import("echarts");
      if (!alive) return;

      if (!ref.current) return;
      chart = echarts.init(ref.current, undefined, { renderer: "canvas" });
      chart.setOption(option, true);

      const onResize = () => chart?.resize();
      window.addEventListener("resize", onResize);

      // Resize after first layout.
      setTimeout(onResize, 0);

      return () => {
        window.removeEventListener("resize", onResize);
      };
    })();

    return () => {
      alive = false;
      if (chart) {
        try {
          chart.dispose();
        } catch {
          // ignore
        }
      }
    };
  }, [option]);

  return (
    <div
      ref={ref}
      className={className ?? "h-64 w-full"}
      style={{ minHeight: 240 }}
    />
  );
}
