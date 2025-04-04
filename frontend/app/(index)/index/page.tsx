"use client";
import { useState, useEffect } from "react";
import {useSession} from "next-auth/react"
import useAuthApi from "lib/fetchApiClient";
import "./test.css";

export default function TestPage() {
  const [data, setData] = useState(null);

  const { data: session, status } = useSession();
  const { authGetApi } = useAuthApi();

  useEffect(() => {
    // Only call if we have a session and the session is authenticated
    if (status === "authenticated" && session?.user?.accessToken) {
      (async () => {
        try {
          const agents = await authGetApi("/agents");
          setData(agents)
        } catch (error) {
          console.error("Error fetching agents:", error);
        }
      })();
    }
  }, [status, session?.user?.accessToken]);

  return (
    <div>
      <h1>Welcome to the index</h1>
      {session ? (
        <>
          {/* Adjust these properties to match your actual session data */}
          <p>User ID: {session.user.id || "Unknown"}</p>
          <p>Username: {session.user.userName || "Unknown"}</p>
          <p>data: {JSON.stringify(data)}</p>

        </>
      ) : (
        <p>You are not logged in.</p>
      )}
    </div>
  );
}

