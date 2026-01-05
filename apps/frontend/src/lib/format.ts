export function fmtPct01(x: number) {
  const v = Math.max(0, Math.min(1, x));
  return `${Math.round(v * 100)}%`;
}

export function fmtDateTime(iso: string) {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString();
}
