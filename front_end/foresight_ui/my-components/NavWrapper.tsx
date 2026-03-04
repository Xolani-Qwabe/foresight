// components/NavWrapper.tsx
"use client";
import React from "react";
import MyNavigation from "./MyNavigation";
import { useAuth } from "@/domain/auth/authContext";

const NavWrapper = () => {
  const { user } = useAuth();

  // This ensures the nav re-renders whenever `user` changes
  React.useEffect(() => {
    console.log("Nav detected user change:", user);
  }, [user]);

  return <MyNavigation />;
};

export default NavWrapper;