"use client";
import React from "react";
import { Agent } from "@/lib/types";

// If you'd like OS icons:
const OS_ICONS: Record<string, string> = {
  windows: "/images/windows.svg",
  linux: "/images/linux.png",
  mac:   "/images/apple.png",
};

interface ClientsCardListProps {
  agents: Agent[];
  onActivate: (agent: Agent) => void;
}

export default function ClientsCardList({ agents, onActivate }: ClientsCardListProps) {
  return (
    <div className="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4">
      {agents.map((agent) => {
        const osKey = (agent.Os || "").toLowerCase();
        const iconSrc = 
          osKey.includes("win") ? OS_ICONS.windows :
          osKey.includes("mac") ? OS_ICONS.mac :
          osKey.includes("lin") ? OS_ICONS.linux :
          "/images/windows.svg"; // default fallback

        return (
          <div className="col" key={agent.AgentId}>
            <div className="card client-card h-100 text-white">
              <div className="card-body d-flex align-items-center">
                {/* OS icon (optional) */}
                <div className="os-icon me-3">
                  <img 
                    src={iconSrc} 
                    alt="OS Icon" 
                    style={{ height: "48px", width: "48px" }} 
                  />
                </div>
                {/* Client info */}
                <div className="flex-grow-1">
                  <h5 className="card-title mb-1 text-info">
                    {agent.HostName}
                  </h5>
                  <p className="card-text mb-0"><strong>OS:</strong> {agent.Os}</p>
                </div>
                {/* Action button */}
                <div>
                  {agent.is_active ? (
                    <button
                      className="btn btn-primary btn-sm"
                      onClick={() => onActivate(agent)}
                    >
                      Activate
                    </button>
                  ) : (
                    <button 
                      className="btn btn-secondary btn-sm" 
                      disabled
                    >
                      Inactive
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
