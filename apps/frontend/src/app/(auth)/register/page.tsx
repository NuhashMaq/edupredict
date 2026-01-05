"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import * as React from "react";
import { z } from "zod";

import { registerStudent } from "@/lib/api";
import { HoverBorderGradient, MultiStepLoader } from "@/components/aceternity";

const schema = z
  .object({
    full_name: z.string().min(2, "Please enter your name"),
    email: z.string().email("Please enter a valid email"),
    password: z.string().min(8, "Use at least 8 characters"),
    confirm: z.string().min(8)
  })
  .refine((v) => v.password === v.confirm, {
    message: "Passwords do not match",
    path: ["confirm"]
  });

type FormState = z.infer<typeof schema>;

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = React.useState<FormState>({
    full_name: "",
    email: "",
    password: "",
    confirm: ""
  });
  const [submitting, setSubmitting] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [step, setStep] = React.useState(0);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setStep(0);

    const parsed = schema.safeParse(form);
    if (!parsed.success) {
      setError(parsed.error.issues[0]?.message ?? "Please check the form.");
      return;
    }

    try {
      setSubmitting(true);
      setStep(0);
      await registerStudent({
        email: parsed.data.email,
        full_name: parsed.data.full_name,
        password: parsed.data.password
      });
      setStep(1);
      router.replace("/login");
    } catch (err) {
      const msg =
        err instanceof Error
          ? err.message
          : "Sign-up failed. Please try again.";
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <MultiStepLoader
        visible={submitting}
        steps={["Creating account", "Redirecting to sign in"]}
        activeIndex={step}
      />
      <h1 className="text-4xl font-semibold tracking-tight">
        <span className="bg-linear-to-r from-(--edp-blue) via-(--edp-orange) to-(--edp-red) bg-clip-text text-transparent">
          Sign up
        </span>
      </h1>
      <p className="mt-2 text-xl leading-8 text-slate-600">Students start here. Admin/Teacher accounts are created by admins.</p>

      <form onSubmit={onSubmit} className="mt-8 grid gap-5">
        <div className="grid gap-2">
          <label className="text-sm font-semibold text-slate-700" htmlFor="full_name">
            Full name
          </label>
          <input
            id="full_name"
            name="full_name"
            autoComplete="name"
            placeholder="Ada Lovelace"
            value={form.full_name}
            onChange={(e) => setForm((s) => ({ ...s, full_name: e.target.value }))}
            className="h-13 w-full rounded-2xl border border-[rgba(20,65,206,0.18)] bg-white/70 px-5 text-lg text-slate-900 outline-none placeholder:text-slate-400 focus:border-[#1441CE] focus:ring-4 focus:ring-[rgba(20,65,206,0.14)]"
          />
        </div>

        <div className="grid gap-2">
          <label className="text-sm font-semibold text-slate-700" htmlFor="email">
            Email
          </label>
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            placeholder="you@school.edu"
            value={form.email}
            onChange={(e) => setForm((s) => ({ ...s, email: e.target.value }))}
            className="h-13 w-full rounded-2xl border border-[rgba(20,65,206,0.18)] bg-white/70 px-5 text-lg text-slate-900 outline-none placeholder:text-slate-400 focus:border-[#1441CE] focus:ring-4 focus:ring-[rgba(20,65,206,0.14)]"
          />
        </div>

        <div className="grid gap-2">
          <label className="text-sm font-semibold text-slate-700" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="new-password"
            placeholder="••••••••"
            value={form.password}
            onChange={(e) => setForm((s) => ({ ...s, password: e.target.value }))}
            className="h-13 w-full rounded-2xl border border-[rgba(20,65,206,0.18)] bg-white/70 px-5 text-lg text-slate-900 outline-none placeholder:text-slate-400 focus:border-[#1441CE] focus:ring-4 focus:ring-[rgba(20,65,206,0.14)]"
          />
          <div className="text-sm text-slate-500">At least 8 characters.</div>
        </div>

        <div className="grid gap-2">
          <label className="text-sm font-semibold text-slate-700" htmlFor="confirm">
            Confirm password
          </label>
          <input
            id="confirm"
            name="confirm"
            type="password"
            autoComplete="new-password"
            placeholder="••••••••"
            value={form.confirm}
            onChange={(e) => setForm((s) => ({ ...s, confirm: e.target.value }))}
            className="h-13 w-full rounded-2xl border border-[rgba(20,65,206,0.18)] bg-white/70 px-5 text-lg text-slate-900 outline-none placeholder:text-slate-400 focus:border-[#1441CE] focus:ring-4 focus:ring-[rgba(20,65,206,0.14)]"
          />
        </div>

        {error ? <div className="text-base text-[#EB615F]">{error}</div> : null}

        <div className="mt-1 flex flex-wrap items-center gap-3">
          <HoverBorderGradient
            type="submit"
            disabled={submitting}
            className={
              "h-13 px-7 text-xl font-semibold " +
              "bg-[linear-gradient(135deg,rgba(20,65,206,0.98),rgba(239,127,96,0.92))] " +
              "shadow-[0_18px_70px_rgba(20,65,206,0.20),0_18px_70px_rgba(239,127,96,0.18)]"
            }
          >
            {submitting ? "Signing up…" : "Sign up"}
          </HoverBorderGradient>
          <Link href="/login" className="text-base text-slate-600 hover:text-(--edp-blue)">
            Back to sign in
          </Link>
        </div>
      </form>
    </div>
  );
}
