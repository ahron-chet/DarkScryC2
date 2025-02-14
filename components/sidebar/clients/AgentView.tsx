"use client";
import React, { useState, useEffect } from "react";
import { Agent } from "@/lib/types";

// Example panels you've already defined
import AgentDetailPanel from "./AgentDetailPanel";
import ShellPanel from "./ShellPanel";
import ModulesTestPanel from "./modules/TestPanel";
import ModulesWifiPasswordsPanel from "./modules/WifiPasswordPanel";
import { initAgentViewDropdowns } from "lib/custome_effects"
import useAuthApi from "@/lib/fetchApiClient";
import FileExplorerPanel from "./modules/FileExplorerPanel";

type ActiveModule =
  | "details"
  | "shell"
  | "modules-test"
  | "modules-collection-passwords-wifi"
  | "modules-collection-files-collectfiles";

interface AgentViewProps {
  agent: Agent;
}


export default function AgentView({ agent }: AgentViewProps) {
  const [activeModule, setActiveModule] = useState<ActiveModule>("details");

  // Switch the displayed panel
  function handleSelect(moduleKey: ActiveModule) {
    setActiveModule(moduleKey);
  }

  const { authGetApi } = useAuthApi()

  // Decide which content to render
  let panelContent = null;
  switch (activeModule) {
    case "shell":
      authGetApi(`/agents/${agent.AgentId}/modules/execution/shell/start_shell`)
      panelContent = <ShellPanel agent={agent} />;
      break;
    case "modules-test":
      panelContent = <ModulesTestPanel agent={agent} />;
      break;
    case "modules-collection-passwords-wifi":
      panelContent = <ModulesWifiPasswordsPanel agent={agent} />;
      break;
    case "modules-collection-files-collectfiles":
      panelContent = <FileExplorerPanel agent={agent} />;
      break;
    case "details":
    default:
      panelContent = <AgentDetailPanel agent={agent} />;
      break;
  }

  useEffect(() => {
    if (document.body.dataset.dropdownInit === "true") return;
    document.body.dataset.dropdownInit = "true";
    initAgentViewDropdowns();
  }, []);


  return (
    <div className="agent-view">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark rounded mb-3">
        <div className="container-fluid">
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <a className={`nav-link ${activeModule === "details" ? "active" : ""}`} style={{ cursor: "pointer" }} onClick={() => handleSelect("details")}>
                Agent Details
              </a>
            </li>
            <li className="nav-item">
              <a className={`nav-link ${activeModule === "shell" ? "active" : ""}`} style={{ cursor: "pointer" }} onClick={() => handleSelect("shell")}>
                Remote Shell
              </a>
            </li>
            <li className="nav-item dropdown">
              <a className={`nav-link dropdown-toggle ${activeModule.startsWith("modules") ? "active" : ""}`} href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Modules
              </a>
              <ul className="dropdown-menu dropdown-menu-dark" data-bs-auto-close="outside">
                <li data-bs-auto-close="outside">
                  <a id="test" className="dropdown-item" style={{ cursor: "pointer" }} onClick={() => handleSelect("modules-test")} data-bs-auto-close="outside">
                    Test
                  </a>
                </li>
                <li className="dropdown-submenu">
                  <a className="dropdown-item dropdown-toggle" style={{ cursor: "pointer" }} >
                    Collection
                  </a>
                  <ul className="dropdown-menu dropdown-menu-dark">
                    <li className="dropdown-submenu">
                      <a className="dropdown-item dropdown-toggle" style={{ cursor: "pointer" }}>
                        Passwords
                      </a>
                      <ul className="dropdown-menu dropdown-menu-dark">
                        <li>
                          <a className="dropdown-item" style={{ cursor: "pointer" }} onClick={() => handleSelect("modules-collection-passwords-wifi")}>
                            WiFi
                          </a>
                        </li>
                      </ul>
                    </li>
                    <li className="dropdown-submenu">
                      <a className="dropdown-item dropdown-toggle" style={{ cursor: "pointer" }}>
                        Files
                      </a>
                      <ul className="dropdown-menu dropdown-menu-dark">
                        <li>
                          <a className="dropdown-item" style={{ cursor: "pointer" }} onClick={() => handleSelect("modules-collection-files-collectfiles")}>
                            File Explorer
                          </a>
                        </li>
                      </ul>
                    </li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </nav>
      {panelContent}
    </div>

  );
}
