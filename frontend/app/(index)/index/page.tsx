"use client";
import { useState, useEffect } from "react";
import api from "@/lib/apiClient";
import { getAccessToken } from "@/lib/authClient";
import "./test.css";

export default function TestPage() {
  const [data, setData] = useState(null);
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    const token = getAccessToken();
    if (!token) return;
    setLoggedIn(true);
    (async () => {
      try {
        const res = await api.get("/agents");
        setData(res.data);
      } catch (error) {
        console.error("Error fetching agents:", error);
      }
    })();
  }, []);

  return (
    <div>
      <h1>Welcome to the index</h1>
      {loggedIn ? (
        <>
          <p>data: {JSON.stringify(data)}</p>
        </>
      ) : (
        <p>You are not logged in.</p>
      )}
    </div>
  );
}

