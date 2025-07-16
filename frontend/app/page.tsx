"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { ensureValidTokens } from "@/lib/authClient";

export default function RootPage() {
  const router = useRouter();

  useEffect(() => {
    const handleRedirect = async () => {
      const ok = await ensureValidTokens();
      if (ok) {
        router.replace("/index");
      } else {
        router.replace("/login?callbackUrl=%2Findex");
      }
    };

    if (typeof window !== "undefined") {
      handleRedirect();
    }
  }, [router]);

  return null;
}
