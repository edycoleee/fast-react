import { create } from "zustand";

const AUTH_STORAGE_KEY = "fast_boiler_auth";

const getInitialAuth = () => {
  if (typeof window === "undefined") {
    return { token: null, user: null };
  }
  const raw = window.localStorage.getItem(AUTH_STORAGE_KEY);
  if (!raw) {
    return { token: null, user: null };
  }
  try {
    const parsed = JSON.parse(raw);
    return {
      token: parsed.token || null,
      user: parsed.user || null
    };
  } catch (_error) {
    return { token: null, user: null };
  }
};

const persistAuth = (authState) => {
  if (typeof window !== "undefined") {
    window.localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(authState));
  }
};

const initialAuth = getInitialAuth();

export const useAuthStore = create((set) => ({
  ...initialAuth,
  isAuthenticated: Boolean(initialAuth.token),
  login: ({ token, user }) =>
    set(() => {
      const next = { token, user, isAuthenticated: true };
      persistAuth({ token, user });
      return next;
    }),
  logout: () =>
    set(() => {
      if (typeof window !== "undefined") {
        window.localStorage.removeItem(AUTH_STORAGE_KEY);
      }
      return { token: null, user: null, isAuthenticated: false };
    })
}));

export { AUTH_STORAGE_KEY };
