"use client";
import React, { useState } from "react";
import useAxiosAuth from "@/lib/hooks/useAxiosAuth";
import useTaskRunner from "@/lib/hooks/useTaskRunner";

interface FileItem {
    Name: string;
    Icon: string | null;
    Size: number;
    LastWriteTimeUtc: string;
    CreationTimeUtc: string;
    Path: string;
}

interface FileDetailModalProps {
    file: FileItem;
    agentId: string;
    onClose: () => void;
}

export default function FileDetailModal({ file, agentId, onClose }: FileDetailModalProps) {
    const [downloadLoading, setDownloadLoading] = useState(false);
    const [downloadError, setDownloadError] = useState<string | null>(null);
    const { getTaskResults, error: task_error, result: task_result } = useTaskRunner();
    
    const axiosAuth = useAxiosAuth()
    async function handleDownload() {
        try {
            setDownloadLoading(true);
            setDownloadError(null);
            const response = await axiosAuth.post<any>(`/agents/${agentId}/modules/collection/files/get_file_base64`,{
                path: file.Path
            })
            const task_response = await getTaskResults(response.data.task_id)
            const data = task_response.result.data.result;
            if (!data.file_base64) throw new Error("No base64 in response");

            const byteCharacters = atob(data.file_base64);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }
            const blob = new Blob([new Uint8Array(byteNumbers)], { type: "application/octet-stream" });
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = file.Name;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);

            setDownloadLoading(false);
        } catch (err) {
            console.error("Download failed:", err);
            setDownloadError("Failed to download file.");
            setDownloadLoading(false);
        }
    }

    return (
        <>
            <div className="modal-backdrop fade show"></div>
            <div className="modal fade show d-block" tabIndex={-1} role="dialog" style={{ zIndex: 9999 }}>
                <div className="modal-dialog modal-dialog-centered" role="document">
                    <div className="modal-content bg-dark text-white" style={{ borderRadius: "16px" }}>

                        <div className="modal-header">
                            <h5 className="modal-title" style={{ fontFamily: "Orbitron, sans-serif" }}>
                                File Details
                            </h5>
                            <button
                                type="button"
                                className="btn-close btn-close-white"
                                aria-label="Close"
                                onClick={onClose}
                            ></button>
                        </div>

                        <div className="modal-body">
                            <p><strong>Name:</strong> {file.Name}</p>
                            <div className="file-path-container">
                                <strong>Path:</strong>
                                <div className="file-path-scrollbar">{file.Path}</div>
                            </div>



                            <p><strong>Size:</strong> {file.Size} bytes</p>
                            <p><strong>Created:</strong> {file.CreationTimeUtc}</p>
                            <p><strong>Last Modified:</strong> {file.LastWriteTimeUtc}</p>
                        </div>

                        {/* Footer with error on the left, buttons on the right */}
                        <div className="modal-footer d-flex w-100 justify-content-between align-items-center">
                            <div>
                                {downloadError && <span className="text-danger me-3">{downloadError}</span>}
                            </div>
                            <div>
                                <button
                                    type="button"
                                    className="btn btn-secondary me-2"
                                    onClick={onClose}
                                >
                                    Close
                                </button>
                                <button
                                    type="button"
                                    className="btn btn-primary"
                                    onClick={handleDownload}
                                    disabled={downloadLoading}
                                >
                                    {downloadLoading ? "Downloading..." : "Download"}
                                </button>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </>
    );
}
