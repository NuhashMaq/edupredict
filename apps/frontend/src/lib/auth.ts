export type TokenPair = {
  access_token: string;
  refresh_token: string;
};

const ACCESS_KEY = "edupredict.access";
const REFRESH_KEY = "edupredict.refresh";

export function getStoredTokens(): TokenPair | null {
  if (typeof window === "undefined") return null;
  const access = window.localStorage.getItem(ACCESS_KEY);
  const refresh = window.localStorage.getItem(REFRESH_KEY);
  if (!access || !refresh) return null;
  return { access_token: access, refresh_token: refresh };
}

export function storeTokens(tokens: TokenPair) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(ACCESS_KEY, tokens.access_token);
  window.localStorage.setItem(REFRESH_KEY, tokens.refresh_token);
}

export function clearTokens() {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(ACCESS_KEY);
  window.localStorage.removeItem(REFRESH_KEY);
}
