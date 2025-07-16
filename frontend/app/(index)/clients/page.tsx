"use client";

import React, { useEffect, useState } from "react";
import api from "@/lib/apiClient";
import { Agent } from "@/lib/types";

import ClientsTabsBar from "@/components/sidebar/clients/ClientsTabsBar";
import ClientsCardList  from "@/components/sidebar/clients/ClientsCardList";
import AgentView from "@/components/sidebar/clients/AgentView";

import "./clients.css";


export default function ClientsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  // Agents that have been "activated" and appear as separate tabs
  const [openAgents, setOpenAgents] = useState<Agent[]>([]);
  // Current tab: "all" or an agent_id
  const [activeTab, setActiveTab] = useState<string>("all");

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get<Agent[]>("/agents");
        setAgents(res.data);
      } catch (err) {
        console.error("Error fetching agents:", err);
      }
    })();
  }, []);

  /** "Activate" means adding an agent's tab if it's active. */
  function handleActivate(agent: Agent) {
    if (!agent.is_active) return; // If agent isn't truly active, ignore or show message
    setOpenAgents((prev) => {
      const alreadyOpen = prev.some((a) => a.agent_id === agent.agent_id);
      return alreadyOpen ? prev : [...prev, agent];
    });
    setActiveTab(agent.agent_id);
  }

  /** Close a specific agent tab. */
  function handleCloseAgent(agent_id: string) {
    setOpenAgents((prev) => prev.filter((a) => a.agent_id !== agent_id));
    if (activeTab === agent_id) setActiveTab("all");
  }

  // Decide what content to show below the tab bar
  let mainContent = null;
  if (activeTab === "all") {
    mainContent = (
      <ClientsCardList agents={agents} onActivate={handleActivate} />
    );
  } else {
    const selectedAgent = openAgents.find((a) => a.agent_id === activeTab);
    mainContent = selectedAgent ? (
      <AgentView agent={selectedAgent} />
    ) : (
      <ClientsCardList agents={agents} onActivate={handleActivate} />
    );
  }

  return (
    
    <div className="container-fluid py-4">
      {/* The top bar with "All Clients" + open agent tabs */}
      <ClientsTabsBar
        allLabel="All Clients"
        openAgents={openAgents}
        activeTab={activeTab}
        onTabClick={(tabId) => setActiveTab(tabId)}
        onCloseAgent={handleCloseAgent}
      />

      <div className="mt-4">{mainContent}</div>
    </div>
  );
}
