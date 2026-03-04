"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { logoutService } from "../auth/logout/service";

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

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined,
);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check for existing session
  useEffect(() => {
    const checkAuth = async () => {
      console.log("Checking session...");
      try {
        const res = await fetch("/api/auth/session", {
          credentials: "include",
        });
        console.log("Session status:", res.status);

        if (res.ok) {
          const data = await res.json();
          console.log("Session user:", data.user);
          setUser(data.user);
        } else {
          console.log("Session failed");
        }
      } catch (error) {
        console.error("Failed to check auth:", error);
      } finally {
        setIsLoading(false);
      }
    };
    checkAuth();
  }, []);

const login = (userData: User) => {
    setUser(userData); // Updates `user` and triggers re-render
  };

  // Centralized logout

  const logout = async () => {
    try {
      await logoutService();
      setUser(null);
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        setUser,
        isLoading,
        isAuthenticated: !!user,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
}
