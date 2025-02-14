"use client";
import React, { useEffect, useState } from "react";
import { Agent } from "@/lib/types";
import useTaskRunner from "@/lib/hooks/useTaskRunnerold";

interface AgentDetailPanelProps {
  agent: Agent;
}

// Example response structure
interface BasicMachineInfo {
  HostName: string;
  OperatingSystem: string;
  OSVersionDetail: string;
  CPU: string;
  RAM: string;
  Disk: string;
  PrimaryIP: string;
  GPU: string;
  AgentStatus: string;
  LastLogin: string;
  LogedInSessions: string[];
}

export default function AgentDetailPanel({ agent }: AgentDetailPanelProps) {

  const { runFetchUntilComplete, error: task_error, result: task_result } = useTaskRunner();
  const [machineInfo, setMachineInfo] = useState<BasicMachineInfo | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);


  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        setLoading(true);
        setError(null);

        const endpoint = `/agents/${agent.AgentId}/modules/collection/machine/basic_mashine_info`;
        const resp = await runFetchUntilComplete(endpoint);
        const data = resp?.result?.data?.result;
        if (mounted) {
          setMachineInfo(data);
          setLoading(false);
        }
      } catch (err: any) {
        console.error("Error fetching agent detail:", err);
        if (mounted) {
          setError("Failed to load machine info");
          setLoading(false);
        }
      }
    })();
    return () => {
      mounted = false;
    };
  }, []);
  if (loading) {
    // A Bootstrap spinner with custom text
    return (
      <div className="d-flex align-items-center text-secondary gap-2">
        <div className="spinner-border spinner-border-sm" role="status" />
        <span>Loading agent details...</span>
      </div>
    );
  }

  if (error || !machineInfo) {
    return <div className="text-danger">{error || "No data available"}</div>;
  }

  // Render card if data is present
  return (
    <div className="card bg-dark text-white" style={{ borderRadius: "16px" }}>
      <div className="card-body">
        <h4 className="card-title text-info" style={{ fontFamily: "Orbitron, sans-serif" }}>
          {machineInfo.HostName}
        </h4>
        <p className="card-text mb-2">
          <strong>Status:</strong> {machineInfo.AgentStatus}
        </p>
        <div className="row g-2">
          <div className="col-12 col-sm-6">
            <strong>OS:</strong> {machineInfo.OperatingSystem}
            <br />
            <small className="text-secondary">{machineInfo.OSVersionDetail}</small>
          </div>
          <div className="col-12 col-sm-6">
            <strong>CPU:</strong> {machineInfo.CPU}
            <br />
            <strong>RAM:</strong> {machineInfo.RAM}
          </div>
          <div className="col-12 col-sm-6">
            <strong>Disk:</strong> {machineInfo.Disk}
            <br />
            <strong>GPU:</strong> {machineInfo.GPU}
          </div>
          <div className="col-12 col-sm-6">
            <strong>Primary IP:</strong> {machineInfo.PrimaryIP}
            <br />
            <strong>Last Login:</strong> {machineInfo.LastLogin}
          </div>
          <div className="col-12">
            <strong>Logged In Sessions:</strong>{" "}
            {machineInfo.LogedInSessions && machineInfo.LogedInSessions.join(", ")}
          </div>
        </div>
      </div>
    </div>
  );
}