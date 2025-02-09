"use client";
import React from "react";
import { Agent } from "@/lib/types";

interface AgentShellPanelProps {
  agent: Agent;
}

/** Stub for future "Remote Shell" feature */
export default function AgentShellPanel({ agent }: AgentShellPanelProps) {
  return (
    <div className="card bg-dark text-white" style={{ borderRadius: "16px" }}>
      <div className="card-body">
        <h4 className="card-title text-warning" style={{ fontFamily: "Orbitron, sans-serif" }}>
          Remote Shell (Coming Soon)
        </h4>
        <p className="card-text">
          Here we'll implement the interactive shell for agent <strong>{agent.HostName}</strong>.
        </p>
      </div>
    </div>
  );
}
