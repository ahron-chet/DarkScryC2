"use client";
import React, { useEffect, useState, useRef } from "react";
import { Agent } from "@/lib/types";
import useAxiosAuth from "@/lib/hooks/useAxiosAuth";
import useTaskRunner from "@/lib/hooks/useTaskRunner";
import Loading from "@/components/Loading";
import { module_descriptior } from "@/lib/models";

interface ProcessRecord {
    ProcessName: string;
    ProcessId: number;
    MemoryUsage: number;
    Owner: string;
    WasInjected: boolean;
}

interface ProcessInjectPanelProps {
    agent: Agent;
    injection_type: InjectionType;
}

type InjectionType = "remote_thread_shellcode";

export default function ProcessInjectPanel({ agent, injection_type }: ProcessInjectPanelProps) {
    const authAxios = useAxiosAuth();
    const { getTaskResults } = useTaskRunner();

    const [processList, setProcessList] = useState<ProcessRecord[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    // For the injection modal
    const [showModal, setShowModal] = useState<boolean>(false);
    const [selectedProc, setSelectedProc] = useState<ProcessRecord | null>(null);

    // For searching
    const [searchText, setSearchText] = useState<string>("");

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

    // Show the injection modal
    function handleInjectClick(proc: ProcessRecord) {
        console.log("Injecting into PID:", proc.ProcessId);
        setSelectedProc(proc);
        setShowModal(true);
    }

    // For now, injection logic is placeholder
    function handleInjectionConfirm() {
        if (!selectedProc) return;
        console.log("Start injection for PID:", selectedProc.ProcessId, "type:", injection_type);
        setShowModal(false);
    }

    // If user uploads shellcode -> handle it. Placeholder for now
    function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
        const file = e.target.files?.[0];
        if (!file) return;
        console.log("Shellcode file selected:", file.name);
        // Optionally read it with FileReader
    }

    // ========== SEARCH FILTER LOGIC ==========
    const filteredProcessList = processList.filter((proc) => {
        const query = searchText.toLowerCase();
        if (!query) return true; // no filter => show all

        // Check process name, owner, or PID
        const pidStr = String(proc.ProcessId);
        return (
            proc.ProcessName.toLowerCase().includes(query) ||
            proc.Owner.toLowerCase().includes(query) ||
            pidStr.includes(query)
        );
    });

    // ========== RENDERING ==========

    if (loading) return <Loading text="Loading processes..." />;
    if (error) return <div className="text-danger">{error}</div>;

    return (
        <>
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

                <div
                    className="card-body p-0 d-flex flex-column"
                    style={{ maxHeight: "70vh", overflowY: "auto" }}
                >
                    {/* A small area for the search bar */}
                    <div className="p-3">
                        <div className="row g-2 align-items-center">
                            <div className="col">
                                <i className="bi bi-search"></i>
                                <input
                                    type="text"
                                    className="form-control form-control-sm bg-secondary text-white border-0"
                                    placeholder="Filter by name, owner, or PID..."
                                    value={searchText}
                                    onChange={(e) => setSearchText(e.target.value)}
                                    style={{maxWidth: "300px", borderRadius:"10px"}}
                                />
                            </div>
                        </div>
                    </div>

                    {/* The table area */}
                    {filteredProcessList.length === 0 ? (
                        <div className="p-3 text-muted">No processes match your search.</div>
                    ) : (
                        <div className="table-responsive">
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
                                    {filteredProcessList.map((proc, idx) => {
                                        const injectedClass = proc.WasInjected ? "table-warning" : "";

                                        return (
                                            <tr key={idx} className={injectedClass}>
                                                <td>{proc.ProcessName}</td>
                                                <td>{proc.ProcessId}</td>
                                                <td>{(proc.MemoryUsage / 1024).toFixed(1)} KB</td>
                                                <td>{proc.Owner || "SYSTEM"}</td>
                                                <td>
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
                    )}
                </div>
            </div>

            {/* The modal for injection explanation + shellcode upload */}
            {showModal && selectedProc && (
                <>
                    <div className="modal-backdrop fade show" />
                    <div
                        className="modal fade show d-block"
                        tabIndex={-1}
                        role="dialog"
                        style={{ zIndex: 9999 }}
                    >
                        <div className="modal-dialog modal-dialog-centered" role="document">
                            <div className="modal-content bg-dark text-white" style={{ borderRadius: 16 }}>
                                {/* Modal Header */}
                                <div className="modal-header">
                                    <h5 className="modal-title" style={{ fontFamily: "Orbitron, sans-serif" }}>
                                        {`Injecting into PID: ${selectedProc.ProcessId}`}
                                    </h5>
                                    <button
                                        type="button"
                                        className="btn-close btn-close-white"
                                        aria-label="Close"
                                        onClick={() => setShowModal(false)}
                                    />
                                </div>

                                {/* Modal Body => technique desc + shellcode upload */}
                                <div className="modal-body">
                                    <p className="text-info">
                                        {module_descriptior[injection_type].desc}
                                    </p>
                                    <p className="text-warning">
                                        {module_descriptior[injection_type].desc}
                                    </p>

                                    <div className="mb-3">
                                        <label className="form-label">Upload Shellcode:</label>
                                        <div className="d-flex align-items-center gap-2">
                                            <input
                                                type="file"
                                                className="form-control form-control-sm bg-secondary text-white border-0"
                                                onChange={handleFileChange}
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* Modal Footer => "Close" + "Inject" */}
                                <div className="modal-footer d-flex justify-content-end">
                                    <button
                                        type="button"
                                        className="btn btn-secondary me-2"
                                        onClick={() => setShowModal(false)}
                                    >
                                        Close
                                    </button>
                                    <button
                                        type="button"
                                        className="btn btn-primary"
                                        onClick={handleInjectionConfirm}
                                    >
                                        Start Injection
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </>
            )}
        </>
    );
}
