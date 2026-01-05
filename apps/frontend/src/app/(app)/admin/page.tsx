"use client";

import Link from "next/link";
import * as React from "react";

import { HoverBorderGradient } from "@/components/aceternity";
import { useSession } from "@/components/session/SessionProvider";
import { GlassCard, GsapReveal } from "@/components/ui";

export default function AdminHomePage() {
  const { me } = useSession();
  const role = me?.role;

  if (role !== "admin") {
    return (
      <div className="rounded-2xl border border-rose-300 bg-rose-50 p-4 text-sm text-rose-700">
        This page is only available to admins.
      </div>
    );
  }

  return (
    <GsapReveal>
      <div className="grid gap-6">
        <div data-gsap="pop">
          <h1 className="text-2xl font-semibold tracking-tight text-slate-900">Admin</h1>
          <p className="mt-2 text-sm text-slate-600">User management and system tools.</p>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <GlassCard data-gsap="pop" className="p-6 sm:p-7" tone="fuchsia">
            <div className="text-sm font-semibold text-slate-900">Users</div>
            <div className="mt-1 text-xs text-slate-600">
              Create users, assign roles, and activate/deactivate accounts.
            </div>
            <div className="mt-4">
              <Link href="/admin/users">
                <HoverBorderGradient>Manage users</HoverBorderGradient>
              </Link>
            </div>
          </GlassCard>

          <GlassCard data-gsap="pop" className="p-6 sm:p-7" tone="cyan">
            <div className="text-sm font-semibold text-slate-900">Engine</div>
            <div className="mt-1 text-xs text-slate-600">
              Run updates, review quality checks, and manage versions.
            </div>
            <div className="mt-4">
              <Link href="/admin/ml">
                <HoverBorderGradient>Open console</HoverBorderGradient>
              </Link>
            </div>
          </GlassCard>
        </div>

        <GlassCard data-gsap="pop" className="p-6 sm:p-7" tone="default">
          <div className="text-sm text-slate-700">
            Tip: use <span className="font-semibold text-slate-900">Import</span> to load academic records first.
          </div>
        </GlassCard>
      </div>
    </GsapReveal>
  );
}