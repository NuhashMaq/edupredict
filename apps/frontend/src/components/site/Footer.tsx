export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="relative z-10 mt-10 border-t border-[rgba(20,65,206,0.14)] bg-white/60 text-base backdrop-blur-xl">
      <div className="mx-auto w-full max-w-screen-2xl px-3 pb-6 pt-3 sm:px-6">
        <div
          aria-hidden
          className="h-px w-full bg-[linear-gradient(90deg,transparent,rgba(20,65,206,0.26),rgba(239,127,96,0.26),rgba(235,97,95,0.26),transparent)]"
        />

        <div className="mt-4 flex flex-col items-center justify-between gap-4 text-center sm:flex-row sm:text-left">
          <div className="flex flex-col items-center gap-3 sm:items-start">
            <div className="grid gap-1">
              <div className="text-slate-500">
                © {year} {" "}
                <span className="font-black tracking-tight text-[1.28em] [font-family:var(--font-logo),var(--font-space),ui-sans-serif,system-ui]">
                  <span className="text-(--edp-blue)">edu</span>
                  <span className="text-(--edp-orange)">predict</span>
                </span>
                <span className="mx-2 text-slate-500">•</span>
                <span className="text-slate-500">AI Student Performance Insights</span>
              </div>
              <div className="text-slate-500">Copyright. All rights are reserved.</div>
            </div>
          </div>

          <div className="grid gap-1 sm:text-right">
            <div className="font-semibold tracking-wide text-slate-500">Created by</div>
            <div className="flex flex-wrap items-baseline justify-center gap-x-2 sm:justify-end">
              <div className="font-black tracking-tight text-slate-900">Mashfiq Naushad,</div>
              <div className="font-semibold text-slate-500">CSE 21 - RUET.</div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
