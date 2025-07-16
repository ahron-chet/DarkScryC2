"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { ensureValidTokens } from "../authClient";

export default function useRequireAuth() {
  const router = useRouter();

  useEffect(() => {
    const verify = async () => {
      const ok = await ensureValidTokens();
      if (!ok) {
        const callback = encodeURIComponent(window.location.pathname);
        router.replace(`/login?callbackUrl=${callback}`);
      }
    };

    if (typeof window !== "undefined") {
      verify();
    }
  }, [router]);
}
