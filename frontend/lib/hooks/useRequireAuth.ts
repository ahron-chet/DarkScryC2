"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import api from "../apiClient";
import {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
} from "../authClient";

export default function useRequireAuth() {
  const router = useRouter();

  useEffect(() => {
    const verify = async () => {
      const access = getAccessToken();
      if (access) return;

      const refresh = getRefreshToken();
      if (refresh) {
        try {
          const res = await api.post("/auth/refresh", {
            refresh_token: refresh,
          });
          setTokens(res.data.access_token, res.data.refresh_token);
          return;
        } catch {
          clearTokens();
        }
      }
      const callback = encodeURIComponent(window.location.pathname);
      router.replace(`/login?callbackUrl=${callback}`);
    };

    if (typeof window !== "undefined") {
      verify();
    }
  }, [router]);
}
