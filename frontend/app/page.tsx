"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/apiClient";
import {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
} from "@/lib/authClient";

export default function RootPage() {
  const router = useRouter();

  useEffect(() => {
    const handleRedirect = async () => {
      const access = getAccessToken();
      if (access) {
        router.replace("/index");
        return;
      }
      const refresh = getRefreshToken();
      if (refresh) {
        try {
          const res = await api.post("/auth/refresh", { refresh_token: refresh });
          setTokens(res.data.access_token, res.data.refresh_token);
          router.replace("/index");
          return;
        } catch {
          clearTokens();
        }
      }
      router.replace("/login?callbackUrl=%2Findex");
    };

    if (typeof window !== "undefined") {
      handleRedirect();
    }
  }, [router]);

  return null;
}
