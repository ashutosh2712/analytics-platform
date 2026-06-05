"use client";

import { useEffect } from "react";

import { useRouter } from "next/navigation";

import { isAuthenticated } from "@/lib/auth";

const ProtectedRoute = ({ children }: any) => {
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/login");
    }
  }, []);

  return children;
};

export default ProtectedRoute;
