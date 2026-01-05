"use client";

import * as React from "react";

export type UserPublic = {
  id: string;
  email: string;
  full_name: string;
  role: "admin" | "teacher" | "student";
};

type SessionState = {
  me: UserPublic | null;
  loading: boolean;
};

const SessionContext = React.createContext<SessionState | null>(null);

export function SessionProvider({
  value,
  children
}: {
  value: SessionState;
  children: React.ReactNode;
}) {
  return (
    <SessionContext.Provider value={value}>{children}</SessionContext.Provider>
  );
}

export function useSession() {
  const ctx = React.useContext(SessionContext);
  if (!ctx) {
    throw new Error("useSession must be used within SessionProvider");
  }
  return ctx;
}
