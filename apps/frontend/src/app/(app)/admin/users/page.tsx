"use client";

import * as React from "react";

import { HoverBorderGradient } from "@/components/aceternity";
import { useSession } from "@/components/session/SessionProvider";
import { GlassCard, GsapReveal } from "@/components/ui";
import { apiFetchWithRefresh } from "@/lib/api";
import type { UserPublicAdmin, UsersList, UserRole } from "@/lib/users";

export default function AdminUsersPage() {
  const { me } = useSession();
  const role = me?.role;

  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [data, setData] = React.useState<UsersList | null>(null);

  const [q, setQ] = React.useState<string>("");
  const [filterRole, setFilterRole] = React.useState<UserRole | "">("");
  const [filterActive, setFilterActive] = React.useState<"" | "true" | "false">("");
  const [offset, setOffset] = React.useState<number>(0);

  const [creating, setCreating] = React.useState(false);
  const [createForm, setCreateForm] = React.useState<{
    email: string;
    full_name: string;
    role: UserRole;
    password: string;
  }>({ email: "", full_name: "", role: "student", password: "" });

  const [savingIds, setSavingIds] = React.useState<Record<string, boolean>>({});

  async function load(nextOffset = offset) {
    setError(null);
    setLoading(true);
    try {
      const qs = new URLSearchParams({
        limit: "50",
        offset: String(nextOffset)
      });
      if (q.trim()) qs.set("q", q.trim());
      if (filterRole) qs.set("role", filterRole);
      if (filterActive) qs.set("is_active", filterActive);

      const res = await apiFetchWithRefresh<UsersList>(`/admin/users?${qs.toString()}`);
      setData(res);
      setOffset(nextOffset);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load users");
    } finally {
      setLoading(false);
    }
  }

  React.useEffect(() => {
    if (role === "admin") {
      void load(0);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [role]);

  async function savePatch(
    userId: string,
    patch: { role?: UserRole; is_active?: boolean; full_name?: string }
  ) {
    setError(null);
    setSavingIds((s) => ({ ...s, [userId]: true }));
    try {
      const updated = await apiFetchWithRefresh<UserPublicAdmin>(`/admin/users/${userId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(patch)
      });

      setData((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          items: prev.items.map((u) => (u.id === updated.id ? updated : u))
        };
      });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to update user");
    } finally {
      setSavingIds((s) => {
        const next = { ...s };
        delete next[userId];
        return next;
      });
    }
  }

  async function createUser() {
    setError(null);
    const email = createForm.email.trim();

    if (!email) {
      setError("Email is required.");
      return;
    }
    if (!createForm.password || createForm.password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    setCreating(true);
    try {
      await apiFetchWithRefresh<UserPublicAdmin>("/admin/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          full_name: createForm.full_name,
          role: createForm.role,
          password: createForm.password
        })
      });

      setCreateForm({ email: "", full_name: "", role: "student", password: "" });
      await load(0);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create user");
    } finally {
      setCreating(false);
    }
  }

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
        <div data-gsap="pop" className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight text-slate-900">Admin · Users</h1>
            <p className="mt-2 text-base text-slate-700">Manage roles and activation status.</p>
          </div>
          <HoverBorderGradient onClick={() => load(0)} disabled={loading}>
            Refresh
          </HoverBorderGradient>
        </div>

        {error ? (
          <div data-gsap="pop" className="rounded-xl border border-rose-300 bg-rose-50 p-4 text-base text-rose-700">
            {error}
          </div>
        ) : null}

        <div className="grid gap-6 md:grid-cols-2">
          <GlassCard data-gsap="pop" className="p-6 sm:p-7" tone="fuchsia">
            <div className="text-base font-semibold text-slate-900">Create user</div>
            <div className="mt-1 text-sm text-slate-700">Admins only. Creates a user with a password.</div>

            <div className="mt-4 grid gap-3">
              <div className="grid gap-2">
                <label className="text-sm font-semibold text-slate-700" htmlFor="create-email">
                  Email
                </label>
                <input
                  id="create-email"
                  value={createForm.email}
                  onChange={(e) => setCreateForm((s) => ({ ...s, email: e.target.value }))}
                  placeholder="student@example.com"
                  className="h-11 w-full rounded-xl border border-slate-200/70 bg-white/70 px-3 text-base text-slate-900 outline-none placeholder:text-slate-400 focus:border-(--edp-blue) focus:ring-4 focus:ring-[rgba(20,65,206,0.14)]"
                />
              </div>

              <div className="grid gap-2">
                <label className="text-sm font-semibold text-slate-700" htmlFor="create-name">
                  Full name (optional)
                </label>
                <input
                  id="create-name"
                  value={createForm.full_name}
                  onChange={(e) => setCreateForm((s) => ({ ...s, full_name: e.target.value }))}
                  placeholder="Jane Doe"
                  className="h-11 w-full rounded-xl border border-slate-200/70 bg-white/70 px-3 text-base text-slate-900 outline-none placeholder:text-slate-400 focus:border-(--edp-blue) focus:ring-4 focus:ring-[rgba(20,65,206,0.14)]"
                />
              </div>

              <div className="grid gap-2">
                <label className="text-sm font-semibold text-slate-700" htmlFor="create-role">
                  Role
                </label>
                <select
                  id="create-role"
                  value={createForm.role}
                  onChange={(e) => setCreateForm((s) => ({ ...s, role: e.target.value as UserRole }))}
                  className="h-11 w-full rounded-xl border border-slate-200/70 bg-white/70 px-3 text-base text-slate-900 outline-none focus:border-(--edp-blue) focus:ring-4 focus:ring-[rgba(20,65,206,0.14)]"
                >
                  <option value="student">student</option>
                  <option value="teacher">teacher</option>
                  <option value="admin">admin</option>
                </select>
              </div>

              <div className="grid gap-2">
                <label className="text-sm font-semibold text-slate-700" htmlFor="create-password">
                  Password
                </label>
                <input
                  id="create-password"
                  type="password"
                  value={createForm.password}
                  onChange={(e) => setCreateForm((s) => ({ ...s, password: e.target.value }))}
                  placeholder="••••••••"
                  className="h-11 w-full rounded-xl border border-slate-200/70 bg-white/70 px-3 text-base text-slate-900 outline-none placeholder:text-slate-400 focus:border-(--edp-blue) focus:ring-4 focus:ring-[rgba(20,65,206,0.14)]"
                />
                <div className="text-sm text-slate-700">Minimum 6 characters.</div>
              </div>

              <div className="flex items-center gap-3">
                <HoverBorderGradient variant="orange" onClick={createUser} disabled={creating}>
                  {creating ? "Creating…" : "Create user"}
                </HoverBorderGradient>
              </div>
            </div>
          </GlassCard>

          <GlassCard data-gsap="pop" className="p-6 sm:p-7" tone="cyan">
            <div className="text-base font-semibold text-slate-900">Find users</div>
            <div className="mt-1 text-sm text-slate-700">Filter by email/name, role, or active status.</div>

            <div className="mt-4 grid gap-3">
              <div className="grid gap-2">
                <label className="text-sm font-semibold text-slate-700" htmlFor="q">
                  Search
                </label>
                <input
                  id="q"
                  value={q}
                  onChange={(e) => setQ(e.target.value)}
                  placeholder="email or name…"
                  className="h-11 w-full rounded-xl border border-slate-200/70 bg-white/70 px-3 text-base text-slate-900 outline-none placeholder:text-slate-400 focus:border-(--edp-blue) focus:ring-4 focus:ring-[rgba(20,65,206,0.14)]"
                />
              </div>

              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                <div className="grid gap-2">
                  <label className="text-sm font-semibold text-slate-700" htmlFor="filter-role">
                    Role
                  </label>
                  <select
                    id="filter-role"
                    value={filterRole}
                    onChange={(e) => setFilterRole(e.target.value as UserRole | "")}
                    className="h-11 w-full rounded-xl border border-slate-200/70 bg-white/70 px-3 text-base text-slate-900 outline-none focus:border-(--edp-blue) focus:ring-4 focus:ring-[rgba(20,65,206,0.14)]"
                  >
                    <option value="">All</option>
                    <option value="student">student</option>
                    <option value="teacher">teacher</option>
                    <option value="admin">admin</option>
                  </select>
                </div>

                <div className="grid gap-2">
                  <label className="text-sm font-semibold text-slate-700" htmlFor="filter-active">
                    Active
                  </label>
                  <select
                    id="filter-active"
                    value={filterActive}
                    onChange={(e) => setFilterActive(e.target.value as "" | "true" | "false")}
                    className="h-11 w-full rounded-xl border border-slate-200/70 bg-white/70 px-3 text-base text-slate-900 outline-none focus:border-(--edp-blue) focus:ring-4 focus:ring-[rgba(20,65,206,0.14)]"
                  >
                    <option value="">All</option>
                    <option value="true">active</option>
                    <option value="false">inactive</option>
                  </select>
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <HoverBorderGradient
                  variant="orange"
                  onClick={() => load(0)}
                  disabled={loading}
                  className={
                    loading
                      ? "bg-white text-slate-500 border-slate-200 ring-slate-200/70"
                      : ""
                  }
                >
                  {loading ? "Searching…" : "Apply filters"}
                </HoverBorderGradient>

                <div className="text-sm text-slate-700">
                  Showing {(data?.items?.length ?? 0)} of {data?.total ?? 0}
                </div>
              </div>
            </div>
          </GlassCard>
        </div>

        <GlassCard data-gsap="pop" className="p-0" tone="default">
          <div className="overflow-x-auto">
            <div className="min-w-220">
              <div className="grid grid-cols-12 gap-3 border-b border-slate-200/70 bg-white/65 px-4 py-3 text-sm font-semibold text-slate-700">
                <div className="col-span-4">Email</div>
                <div className="col-span-3">Name</div>
                <div className="col-span-2">Role</div>
                <div className="col-span-2">Active</div>
                <div className="col-span-1 text-right">Save</div>
              </div>

              {(data?.items ?? []).map((u) => (
                <UserRow key={u.id} user={u} saving={Boolean(savingIds[u.id])} onSave={savePatch} />
              ))}

              {!data?.items?.length ? (
                <div className="px-4 py-6 text-base text-slate-700">No users found.</div>
              ) : null}
            </div>
          </div>
        </GlassCard>

        <div data-gsap="pop" className="flex items-center justify-between gap-3">
          <div className="text-sm text-slate-700">Offset: {offset}</div>
          <div className="flex items-center gap-2">
            <HoverBorderGradient
              variant="orange"
              className="px-3 py-2 text-sm"
              disabled={loading || offset <= 0}
              onClick={() => load(Math.max(0, offset - 50))}
            >
              Prev
            </HoverBorderGradient>
            <HoverBorderGradient
              variant="blue"
              className="px-3 py-2 text-sm"
              disabled={loading || (data ? offset + (data.items?.length ?? 0) >= data.total : true)}
              onClick={() => load(offset + 50)}
            >
              Next
            </HoverBorderGradient>
          </div>
        </div>
      </div>
    </GsapReveal>
  );
}

function UserRow({
  user,
  saving,
  onSave
}: {
  user: UserPublicAdmin;
  saving: boolean;
  onSave: (userId: string, patch: { role?: UserRole; is_active?: boolean; full_name?: string }) => Promise<void>;
}) {
  const [fullName, setFullName] = React.useState<string>(user.full_name);
  const [role, setRole] = React.useState<UserRole>(user.role);
  const [active, setActive] = React.useState<boolean>(user.is_active);

  React.useEffect(() => {
    setFullName(user.full_name);
    setRole(user.role);
    setActive(user.is_active);
  }, [user.full_name, user.role, user.is_active]);

  const dirty = fullName !== user.full_name || role !== user.role || active !== user.is_active;

  return (
    <div className="grid grid-cols-12 items-center gap-3 border-b border-slate-200/70 px-4 py-3 text-base text-slate-800 transition-colors hover:bg-[rgba(20,65,206,0.04)] last:border-b-0">
      <div className="col-span-4 truncate">{user.email}</div>
      <div className="col-span-3">
        <input
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          placeholder="(no name)"
          className="h-9 w-full rounded-xl border border-slate-200/70 bg-white/70 px-2 text-base text-slate-900 outline-none placeholder:text-slate-400 focus:border-(--edp-blue) focus:ring-4 focus:ring-[rgba(20,65,206,0.14)]"
        />
      </div>
      <div className="col-span-2">
        <select
          className="h-9 w-full rounded-xl border border-slate-200/70 bg-white/70 px-2 text-base text-slate-900 outline-none focus:border-(--edp-blue) focus:ring-4 focus:ring-[rgba(20,65,206,0.14)]"
          value={role}
          onChange={(e) => setRole(e.target.value as UserRole)}
        >
          <option value="student">student</option>
          <option value="teacher">teacher</option>
          <option value="admin">admin</option>
        </select>
      </div>
      <div className="col-span-2">
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={active}
            onChange={(e) => setActive(e.target.checked)}
            className="h-4 w-4 rounded border border-slate-300 bg-white accent-(--edp-blue)"
          />
          <span className="text-sm text-slate-700">active</span>
        </label>
      </div>
      <div className="col-span-1 flex justify-end">
        <HoverBorderGradient
          roundedClassName="rounded-xl"
          variant="blue"
          className={
            "px-3 py-2 text-sm " +
            (dirty
              ? "border border-[#00B300] bg-[#00B300] text-white ring-1 ring-[rgba(0,179,0,0.30)] hover:bg-[#009A00]"
              : "bg-white text-slate-900 border-slate-200 ring-slate-200/70")
          }
          disabled={!dirty || saving}
          onClick={() => onSave(user.id, { full_name: fullName, role, is_active: active })}
        >
          {saving ? "Saving…" : "Save"}
        </HoverBorderGradient>
      </div>
    </div>
  );
}
