'use client';
import { createContext, useContext, useEffect, useState } from "react";
import { logoutService } from "@/domain/auth/logout/service"; // adjust path
import { loginService } from "@/domain/auth/login/service";   // adjust path

export interface User {
  id: string;
  username: string;
  email: string;
  credits: number;
}

interface AuthContextType {
  user: User | null;
  setUser: (user: User | null) => void;
  isLoading: boolean;
  isAuthenticated: boolean;
  logout: () => Promise<void>;

}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check existing session on mount
  useEffect(() => {
    const checkSession = async () => {
      try {
        const res = await fetch("/api/auth/session", { credentials: "include" });
        if (res.ok) {
          const data = await res.json();
          setUser(data.user); // <-- sets user state immediately
        }
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    checkSession();
  }, []);

  const logout = async () => {
    try {
      await logoutService();
      setUser(null); // <-- removes user immediately
    } catch (err) {
      console.error(err);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const data = await loginService(email, password); // should return user info
      setUser(data.user); // <-- **update context immediately**
    } catch (err) {
      console.error("Login failed:", err);
      throw err;
    }
  };

  return (
    <AuthContext.Provider value={{ user, setUser, isLoading, isAuthenticated: !!user, logout, login }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}