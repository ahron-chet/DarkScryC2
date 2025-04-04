"use client";

import React, { useEffect, useState } from "react";
import { useSession } from "next-auth/react";

import useAuthApi from "lib/fetchApiClient";
import { Agent } from "@/lib/types";

import ClientsTabsBar from "@/components/sidebar/clients/ClientsTabsBar";
import ClientsCardList  from "@/components/sidebar/clients/ClientsCardList";
import AgentView from "@/components/sidebar/clients/AgentView";

import "./clients.css";


export default function ClientsPage() {
  const { data: session, status } = useSession();
  const { authGetApi } = useAuthApi();

  const [agents, setAgents] = useState<Agent[]>([]);
  // Agents that have been "activated" and appear as separate tabs
  const [openAgents, setOpenAgents] = useState<Agent[]>([]);
  // Current tab: "all" or an AgentId
  const [activeTab, setActiveTab] = useState<string>("all");

  useEffect(() => {
    if (status === "authenticated" && session?.user.accessToken) {
      (async () => {
        try {
          const fetched = await authGetApi("/agents");
          setAgents(fetched || []);
        } catch (err) {
          console.error("Error fetching agents:", err);
        }
      })();
    }
  }, [status, session?.user.accessToken]);

  /** "Activate" means adding an agent's tab if it's active. */
  function handleActivate(agent: Agent) {
    if (!agent.is_active) return; // If agent isn't truly active, ignore or show message
    setOpenAgents((prev) => {
      const alreadyOpen = prev.some((a) => a.AgentId === agent.AgentId);
      return alreadyOpen ? prev : [...prev, agent];
    });
    setActiveTab(agent.AgentId);
  }

  /** Close a specific agent tab. */
  function handleCloseAgent(agentId: string) {
    setOpenAgents((prev) => prev.filter((a) => a.AgentId !== agentId));
    if (activeTab === agentId) setActiveTab("all");
  }

  // Decide what content to show below the tab bar
  let mainContent = null;
  if (activeTab === "all") {
    mainContent = (
      <ClientsCardList agents={agents} onActivate={handleActivate} />
    );
  } else {
    const selectedAgent = openAgents.find((a) => a.AgentId === activeTab);
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
