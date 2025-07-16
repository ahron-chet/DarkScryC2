"use client";
import { useState, useEffect } from "react";
import api from "@/lib/apiClient";
import useRequireAuth from "@/lib/hooks/useRequireAuth";
import "./test.css";

export default function TestPage() {
  useRequireAuth();
  const [data, setData] = useState(null);

  useEffect(() => {
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
      <p>data: {JSON.stringify(data)}</p>
    </div>
  );
}

