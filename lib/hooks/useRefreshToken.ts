"use client";

import axios from "lib/axios";
import { signIn, useSession } from "next-auth/react";

export const useRefreshToken = () => {
  const { data: session } = useSession();

  const refreshToken = async () => {
    const res = await axios.post("/api/v2/auth/refresh", {
      refresh_token: session?.user.refreshToken,
    });
    
    if (session) session.user.accessToken = res.data.token;
    else signIn();
  };
  return refreshToken;
};
