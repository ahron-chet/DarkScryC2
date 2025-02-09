"use client";
import React from "react";
import { Agent } from "@/lib/types";

interface ModulesPasswordsPanelProps {
  agent: Agent;
}

/** A placeholder for "Collection - Passwords" module */
export default function ModulesWifiPasswordsPanel({ agent }: ModulesPasswordsPanelProps) {
  return (
    <div className="card bg-dark text-white">
      <div className="card-body">
        <h4 className="card-title text-info">Collection - Passwords</h4>
        <p className="card-text">
          Soon, we'll implement the logic to collect stored passwords on <strong>{agent.HostName}</strong>
        </p>
      </div>
    </div>
  );
}
