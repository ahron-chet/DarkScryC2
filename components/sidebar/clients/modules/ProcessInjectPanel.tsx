"use client";
import React, { useEffect, useState } from "react";
import { Agent } from "@/lib/types";
import useAxiosAuth from "@/lib/hooks/useAxiosAuth";
import useTaskRunner from "@/lib/hooks/useTaskRunner";
import Loading from "@/components/Loading";

interface ProcessRecord {
    ProcessName: string;
    ProcessId: number;
    MemoryUsage: number;
    Owner: string;
    WasInjected: boolean;
}

interface ProcessInjectPanelProps {
    agent: Agent;
    injection_type: InjectionType
}

type InjectionType =
    | "remote_thread_shellcode";

export default function ProcessInjectPanel({ agent, injection_type }: ProcessInjectPanelProps) {
    const authAxios = useAxiosAuth();

    const [processList, setProcessList] = useState<ProcessRecord[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const { getTaskResults } = useTaskRunner();

    // On mount => fetch processes
    useEffect(() => {
        fetchProcesses();
    }, [agent.AgentId]);

    async function fetchProcesses() {
        try {
            setLoading(true);
            setError(null);

            const resp = await authAxios.get<any>(
                `/agents/${agent.AgentId}/modules/collection/process/enumerate_processes`
            );
            const processes = await getTaskResults(resp.data.task_id);
            setProcessList(processes || []);
            setLoading(false);
        } catch (err) {
            console.error("Failed to fetch processes:", err);
            setError("Error loading process list.");
            setLoading(false);
        }
    }

    function handleRefresh() {
        fetchProcesses();
    }

    // For now, the injection logic is empty.
    function handleInjectClick(proc: ProcessRecord) {
        console.log("Injecting into PID:", proc.ProcessId);
        switch (injection_type) {
            case "remote_thread_shellcode":
                console.log("remote_thread_shellcode");
                break
            default:
                console.error("Unknown injection_type")
                break;
        }
    }

    if (loading) {
        return <Loading text="Loading processes..." />;
    }
    if (error) {
        return <div className="text-danger">{error}</div>;
    }
    if (processList.length === 0) {
        return (
            <div className="card bg-dark text-white" style={{ borderRadius: 16 }}>
                <div className="card-body">
                    No processes found.
                </div>
            </div>
        );
    }

    return (
        <div className="card bg-dark text-white" style={{ borderRadius: 16 }}>
            <div className="card-header d-flex justify-content-between align-items-center">
                <h5 className="mb-0" style={{ fontFamily: "Orbitron, sans-serif" }}>
                    Process Injection
                </h5>
                <button
                    className="btn btn-sm btn-secondary d-flex align-items-center"
                    onClick={handleRefresh}
                >
                    <i className="bi bi-arrow-clockwise me-1" />
                    Refresh
                </button>
            </div>

            {/* We do vertical scroll fix on card-body; horizontal scroll with .table-responsive */}
            <div
                className="card-body p-0 d-flex flex-column"
                style={{ maxHeight: "70vh", overflowY: "auto" }}
            >
                <div className="table-responsive">
                    {/* "credential-table table-fixed" => your existing "cyber" table classes */}
                    <table className="table table-dark table-hover table-sm mb-0 credential-table table-fixed">
                        <thead>
                            <tr>
                                <th style={{ width: "30%" }}>Name</th>
                                <th style={{ width: "10%" }}>PID</th>
                                <th style={{ width: "15%" }}>Memory</th>
                                <th style={{ width: "30%" }}>Owner</th>
                                <th style={{ width: "15%" }}>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {processList.map((proc, idx) => {
                                // If WasInjected => optionally highlight row?
                                // We'll just do an inline style or a class.
                                const injectedClass = proc.WasInjected ? "table-warning" : "";

                                return (
                                    <tr key={idx} className={injectedClass}>
                                        <td>{proc.ProcessName}</td>
                                        <td>{proc.ProcessId}</td>
                                        <td>{(proc.MemoryUsage / 1024).toFixed(1)} KB</td>
                                        <td>{proc.Owner || "SYSTEM"}</td>
                                        <td>
                                            {/* "Inject" icon button - no real logic yet */}
                                            <button
                                                className="btn btn-sm btn-primary d-flex align-items-center"
                                                onClick={() => handleInjectClick(proc)}
                                            >
                                                <i className="bi bi-capslock-fill me-1"></i>
                                                Inject
                                            </button>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
