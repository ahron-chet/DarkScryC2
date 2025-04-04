"use client";
import React from "react";
import { Agent } from "@/lib/types";

interface ModulesTestPanelProps {
  agent: Agent;
}

/** A simple placeholder for the "Test" module */
export default function ModulesTestPanel({ agent }: ModulesTestPanelProps) {
  return (
    <div className="card bg-dark text-white">
      <div className="card-body">
        <h4 className="card-title text-warning">Test Module</h4>
        <p className="card-text">
          This is a placeholder "Test" module for agent <strong>{agent.HostName}</strong>.
        </p>
      </div>
    </div>
  );
}
