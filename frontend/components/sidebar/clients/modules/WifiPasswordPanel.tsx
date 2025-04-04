"use client";
import React, { useEffect, useState } from "react";
import { Agent } from "@/lib/types";
import useTaskRunner from "@/lib/hooks/useTaskRunner";
import useAxiosAuth from "@/lib/hooks/useAxiosAuth";
import Loading from "@/components/Loading";

interface WifiPasswordRecord {
  SSIDName: string | null;
  Password: string | null;
  Authentication: string | null;
  Cipher: string | null;
}

interface WifiPasswordsPanelProps {
  agent: Agent;
}


export default function WifiPasswordsPanel({ agent }: WifiPasswordsPanelProps) {
  const { getTaskResults } = useTaskRunner();
  const authAxios = useAxiosAuth()
  const [wifiList, setWifiList] = useState<WifiPasswordRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchWifiPasswords();
  }, [agent.AgentId]);

  async function fetchWifiPasswords() {
    try {
      setLoading(true);
      setError(null);

      // Example: GET or POST. If GET:
      const response = await authAxios.get<any>(`/agents/${agent.AgentId}/modules/collection/passwords/wifi_baisc_info`);
      const data: WifiPasswordRecord[] = await getTaskResults(response.data.task_id);

      setWifiList(data || []);
      setLoading(false);
    } catch (err) {
      console.error("Failed to fetch Wi-Fi passwords:", err);
      setError("Error loading Wi-Fi password data.");
      setLoading(false);
    }
  }

  function handleRefresh() {
    fetchWifiPasswords();
  }

  function isNoPassword(pwd: string | null | undefined): boolean {
    return pwd === null || pwd === undefined || pwd.toLowerCase() === "none";
  }
  function isUnsafeProtocol(auth: string | null | undefined): boolean {
    if (!auth) return false;
    const lower = auth.toLowerCase();
    return lower.includes("open") || lower.includes("wep");
  }
  if (loading) {
    return <Loading text={"Loading Wifi passwords..."} />;
  }

  if (error) {
    return <div className="text-danger">{error}</div>;
  }

  return (
    <div className="general-panel card bg-dark text-white wifi-cred-panel" style={{ borderRadius: 16 }}>
      <div className="card-header d-flex justify-content-between align-items-center">
        <h5 className="mb-0" style={{ fontFamily: "Orbitron, sans-serif" }}>
          Wi-Fi Passwords
        </h5>
        <button
          className="btn btn-sm btn-secondary d-flex align-items-center"
          onClick={handleRefresh}
        >
          <i className="bi bi-arrow-clockwise me-1" />
          Refresh
        </button>
      </div>

      <div className="card-body p-0 general-panel">
        {wifiList.length === 0 ? (
          <div className="p-3 text-muted">No Wi-Fi networks found.</div>
        ) : (
          /* .table-responsive => horizontal scroll on small screens. */
          <div className="table-responsive">
            {/* Combine our "credential-table" class with "table-fixed" to ensure column widths. */}
            <table className="table table-dark table-hover table-sm mb-0 credential-table table-fixed">
              <thead>
                <tr>
                  <th>SSID</th>
                  <th className="cred-password-col">Password</th>
                  <th>Authentication</th>
                  <th>Cipher</th>
                </tr>
              </thead>
              <tbody>
                {wifiList.map((wifi, idx) => {
                  // If password is null => "None"
                  const pwd = wifi.Password ?? "None";

                  // We apply a custom class if password is missing or auth is unsafe
                  const pwdClass = isNoPassword(pwd) ? "unsafe-credential" : "";
                  const authClass = isUnsafeProtocol(wifi.Authentication)
                    ? "unsafe-protocol"
                    : "";

                  return (
                    <tr key={idx}>
                      <td>{wifi.SSIDName || "Unknown"}</td>
                      <td className={`cred-password-col ${pwdClass}`}>
                        {pwd}
                      </td>
                      <td className={authClass}>{wifi.Authentication || "N/A"}</td>
                      <td>{wifi.Cipher || "N/A"}</td>
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