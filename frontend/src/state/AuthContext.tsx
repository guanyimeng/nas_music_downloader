import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { login as apiLogin, me as apiMe, logout as apiLogout, registerUser as apiRegister } from "../api/client";
import type { UserResponse } from "../types";

type AuthContextType = {
  user: UserResponse | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Bootstrap auth state from localStorage
  useEffect(() => {
    const t = localStorage.getItem("token");
    if (!t) {
      setLoading(false);
      return;
    }
    setToken(t);
    // Try to fetch current user
    apiMe()
      .then((u) => setUser(u))
      .catch(() => {
        // token invalid
        localStorage.removeItem("token");
        setToken(null);
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const doLogin = async (username: string, password: string) => {
    const tok = await apiLogin(username, password);
    localStorage.setItem("token", tok.access_token);
    setToken(tok.access_token);
    const u = await apiMe();
    setUser(u);
  };

  const doRegister = async (username: string, email: string, password: string) => {
    await apiRegister({ username, email, password });
    // Auto-login after successful registration
    await doLogin(username, password);
  };

  const doLogout = async () => {
    try {
      await apiLogout();
    } catch {
      // ignore server errors during logout
    }
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  const value = useMemo<AuthContextType>(
    () => ({
      user,
      token,
      isAuthenticated: !!token && !!user,
      loading,
      login: doLogin,
      register: doRegister,
      logout: doLogout
    }),
    [user, token, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
