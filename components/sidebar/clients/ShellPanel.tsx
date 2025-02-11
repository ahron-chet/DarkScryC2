"use client";
import React, { useEffect, useRef, useState } from "react";
import { Agent } from "@/lib/types";
import { useSession } from "next-auth/react";
import { useShellWebSocket } from "@/lib/hooks/useShellWebSocket";

interface ShellPanelProps {
  agent: Agent;
}


export default function ShellPanel({ agent }: ShellPanelProps) {
  const { data: session } = useSession();
  const accessToken = session?.user?.accessToken || "";

  // Shell Type (File dropdown)
  const [shellType, setShellType] = useState<"powershell" | "cmd">("powershell");
  // User placeholder
  const [currentUser, setCurrentUser] = useState("Test User");
  // Chat messages
  const [chatLog, setChatLog] = useState<{ role: "user" | "server"; text: string }[]>([]);
  // Input
  const [inputVal, setInputVal] = useState("");

  // Connect to your shell WebSocket
  const { sendMessage, connectionStatus } = useShellWebSocket({
    agentId: agent.AgentId,
    accessToken,
    onMessage: (serverMsg: string) => {
      setChatLog((prev) => [...prev, { role: "server", text: serverMsg }]);
    },
  });

  // Auto-scroll to bottom on new messages
  const chatBodyRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [chatLog]);

  function handleSend() {
    if (!inputVal.trim()) return;
    // Add user message
    setChatLog((prev) => [...prev, { role: "user", text: inputVal.trim() }]);
    // Send via WS
    sendMessage(inputVal.trim());
    setInputVal("");
  }

  return (
    // "shell-panel" is a custom class for advanced styling; 
    // use "d-flex flex-column" for Bootstrap flex layout.
    <div className="card shell-panel bg-dark text-white d-flex flex-column">
      {/* --- TOP BAR --- */}
      <div className="card-header shell-panel-header d-flex align-items-center justify-content-between">
        
        {/* File dropdown */}
        <div className="btn-group">
          <button className="btn btn-sm btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
            File: {shellType}
          </button>
          <ul className="dropdown-menu dropdown-menu-dark">
            <li><a className="dropdown-item" onClick={() => setShellType("powershell")}>PowerShell</a></li>
            <li><a className="dropdown-item" onClick={() => setShellType("cmd")}>CMD</a></li>
          </ul>
        </div>

        {/* Connection status badge */}
        <span className="badge bg-info bg-opacity-75">{connectionStatus}</span>

        {/* User dropdown */}
        <div className="btn-group">
          <button className="btn btn-sm btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
            {currentUser}
          </button>
          <ul className="dropdown-menu dropdown-menu-dark dropdown-menu-end">
            <li><a className="dropdown-item" onClick={() => setCurrentUser("Test User")}>Test User</a></li>
            {/* Future dynamic user listing */}
          </ul>
        </div>
      </div>

      {/* --- CHAT BODY --- */}
      {/* "flex-grow-1" ensures this area expands, "shell-chat-body" handles scroll & custom styling */}
      <div ref={chatBodyRef} className="shell-chat-body flex-grow-1 p-3 overflow-auto">
        {chatLog.length === 0 ? (
          <p className="text-muted">No messages yet. Type a command below...</p>
        ) : (
          chatLog.map((msg, idx) => {
            const isUser = msg.role === "user";
            return (
              <div key={idx} className={`mb-2 d-flex ${isUser ? "justify-content-end" : "justify-content-start"}`}>
                <div className={`shell-message ${isUser ? "shell-message-user" : "shell-message-server"}`}>
                  {msg.text}
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* --- FOOTER (Input) --- */}
      <div className="card-footer shell-panel-footer p-2">
        <div className="d-flex gap-2">
          <input
            className="form-control form-control-sm"
            placeholder="Type a command..."
            value={inputVal}
            onChange={(e) => setInputVal(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSend();
            }}
          />
          <button className="btn btn-sm btn-primary" onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
}