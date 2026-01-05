import Image from "next/image";

import { BackgroundBeams, DottedGlowBackground, LampSectionHeader } from "@/components/aceternity";
import { BrandLogo } from "@/components/site/BrandLogo";

const AUTH_BG =
  "https://images.pexels.com/photos/5905484/pexels-photo-5905484.jpeg?auto=compress&cs=tinysrgb&w=2400";

export default function AuthLayout({
  children
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <main className="relative min-h-screen overflow-hidden text-slate-900">
      <div className="pointer-events-none absolute inset-0">
        <Image
          src={AUTH_BG}
          alt=""
          fill
          priority
          sizes="100vw"
          unoptimized
          className="object-cover opacity-18 brightness-110 saturate-110"
        />
        <div aria-hidden className="absolute inset-0 bg-[rgba(250,222,221,0.88)]" />
      </div>

      <BackgroundBeams className="opacity-75" />
      <DottedGlowBackground className="opacity-45" />
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(900px_420px_at_18%_20%,rgba(20,65,206,0.12),transparent_60%),radial-gradient(900px_420px_at_82%_24%,rgba(239,127,96,0.14),transparent_60%),radial-gradient(1100px_560px_at_55%_88%,rgba(235,97,95,0.10),transparent_62%)]"
      />

      <div className="relative mx-auto w-full max-w-screen-2xl px-3 pb-16 pt-8 sm:px-6">
        <header className="flex flex-wrap items-center justify-between gap-3">
          <BrandLogo />
          <div className="edp-welcome-glow text-2xl font-semibold text-slate-700">Welcome</div>
        </header>

        <div className="mt-8 grid min-h-[calc(100vh-220px)] gap-8 lg:grid-cols-2 lg:items-center">
          <section className="p-0">
            <LampSectionHeader
              align="left"
              eyebrow="WELCOME"
              title={
                <>
                  <span className="block text-6xl font-black tracking-tight sm:text-7xl lg:text-7xl">
                    Sign in to continue.
                  </span>
                  <span className="mt-3 block">
                    <span className="edp-blink-2s bg-linear-to-r from-[#1441CE] via-[#EF7F60] to-[#EB615F] bg-clip-text text-5xl font-black tracking-tight text-transparent sm:text-6xl lg:text-6xl">
                      Stay aligned with progress.
                    </span>
                  </span>
                </>
              }
              subtitle={
                <>
                  Access your account and continue your work with a clear, distraction-free experience.
                </>
              }
            />
          </section>

          <div className="grid gap-6">
            <section className="rounded-2xl border border-[rgba(20,65,206,0.14)] bg-white/70 p-7 sm:p-9">{children}</section>

            <div className="flex items-start gap-3 px-1">
              <input
                id="agree"
                name="agree"
                type="checkbox"
                defaultChecked
                className="mt-0.5 h-4 w-4 rounded border border-[rgba(20,65,206,0.24)] accent-[#1441CE]"
              />
              <label htmlFor="agree" className="text-sm text-slate-600">
                By continuing, you agree to our{" "}
                <span className="font-semibold text-slate-700">Terms</span> and{" "}
                <span className="font-semibold text-slate-700">Privacy Policy</span>.
              </label>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
