"use client";
import { useState, useEffect } from "react";
import api from "@/lib/apiClient";
import { Agent } from "@/lib/types";
import "./test.css";

export default function IndexPage() {
  const [data, setData] = useState<Agent[] | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get<Agent[]>("/agents");
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

