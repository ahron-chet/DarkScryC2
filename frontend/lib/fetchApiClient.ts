"use client"; // Ensure this file is treated as a client component in Next.js

import { useSession, signIn, signOut } from "next-auth/react";


function useAuthApi() {
  const { data: session, update } = useSession();

  // Function to handle refreshing the token
  const refreshToken = async (refreshToken: string) => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_DJANGO_API_URL_V2}/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!res.ok) {
      signOut({callbackUrl:"/"});
      throw new Error("Failed to refresh token");
    }

    const data = await res.json();
    console.log("Refresh token response:", data);
    return data.accessToken;
  };

  // The main GET wrapper which refreshes the token if needed
  const authGetApi = async (url: string) => {
    if (!session?.user?.accessToken) {
      // If there's no valid session or accessToken, you may want to re-authenticate:
      // signIn() or throw an error
      throw new Error("No valid user session or access token");
    }
    console.log("process.env.NEXT_PUBLIC_DJANGO_API_URL_V2", process.env.NEXT_PUBLIC_DJANGO_API_URL_V2)
    let res = await fetch(`${process.env.NEXT_PUBLIC_DJANGO_API_URL_V2}${url}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${session.user.accessToken}`,
      },
    });

    // If unauthorized, attempt to refresh the token and retry once
    if (res.status === 401 && session?.user?.refreshToken) {
      try {
        const newAccessToken = await refreshToken(session.user.refreshToken);

        // Update the session in the client to store the new access token
        await update({
          ...session,
          user: {
            ...session.user,
            accessToken: newAccessToken,
          },
        });

        // Retry the fetch with the new token
        console.log(process.env.NEXT_PUBLIC_DJANGO_API_URL_V2)
        res = await fetch(`${process.env.NEXT_PUBLIC_DJANGO_API_URL_V2}${url}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${newAccessToken}`,
          },
        });
      } catch (err) {
        console.error("Token refresh failed:", err);
        // Optionally, force user to sign in again
        // signIn();
        throw err;
      }
    }

    // Finally return JSON response
    if (!res.ok) {
      throw new Error(`Fetch failed with status ${res.status}`);
    }

    return await res.json();
  };

  return { authGetApi };
}

export default useAuthApi;


