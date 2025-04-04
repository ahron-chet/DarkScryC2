"use client";
import React from "react";
import { Agent } from "@/lib/types";

interface ClientsTabsBarProps {
  allLabel: string;
  openAgents: Agent[];
  activeTab: string;
  onTabClick: (tabId: string) => void;
  onCloseAgent: (agentId: string) => void;
}

/**
 * Renders a bar of "All Clients" + open agent tabs. 
 * Each agent tab can be closed or clicked.
 */
export default function ClientsTabsBar({
  allLabel,
  openAgents,
  activeTab,
  onTabClick,
  onCloseAgent,
}: ClientsTabsBarProps) {
  return (
    <div className="d-flex flex-wrap align-items-center gap-2">
      <button
        className={`btn btn-sm ${activeTab === "all" ? "btn-primary" : "btn-secondary"}`}
        onClick={() => onTabClick("all")}
      >
        {allLabel}
      </button>

      {openAgents.map((agent) => {
        const isActive = agent.AgentId === activeTab;
        return (
          <div
            className={`btn-group btn-group-sm ${isActive ? "active-tab-group" : ""}`}
            key={agent.AgentId}
          >
            <button
              className={`btn ${isActive ? "btn-primary" : "btn-secondary"}`}
              onClick={() => onTabClick(agent.AgentId)}
            >
              {agent.HostName}
            </button>
            <button
              className={`btn ${isActive ? "btn-primary" : "btn-secondary"}`}
              onClick={() => onCloseAgent(agent.AgentId)}
            >
              <i className="bi bi-x" />
            </button>
          </div>
        );
      })}
    </div>
  );
}
