"use client";
import React, { useEffect, useRef, useState } from "react";
import { Agent } from "@/lib/types";
import FileDetailModal from "./FileDetailModal";
import { segmentsToPath, pathToSegments } from "@/utils/files";
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

interface DirectoriesData {
  Items: string[];
}

interface FileExplorerResponse {
  Files: FileItem[];
  Directories: DirectoriesData;
  RootPath: string;
}

interface FileExplorerPanelProps {
  agent: Agent;
}

export default function FileExplorerPanel({ agent }: FileExplorerPanelProps) {
  const axiosAuth = useAxiosAuth();

  // Current "canonical" path
  const [pathSegments, setPathSegments] = useState<string[]>([]);
  // Directory & file listing
  const [directories, setDirectories] = useState<string[]>([]);
  const [files, setFiles] = useState<FileItem[]>([]);
  // UI states
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  // Path typed by user
  const [customPath, setCustomPath] = useState("");
  // Selected file detail
  const [selectedFile, setSelectedFile] = useState<FileItem | null>(null);

  // Hidden file input for "Upload"
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const { getTaskResults } = useTaskRunner();

  // On mount => load root
  useEffect(() => {
    fetchDirectory([]);
  }, [agent.AgentId]);

  async function fetchDirectory(segments: string[]) {
    try {
      setLoading(true);
      setError(null);

      const pathString = segmentsToPath(segments);

      // The server expects a POST with { path }, returning { RootPath, Directories, Files }
      const response = await axiosAuth.post<FileExplorerResponse>(
        `/agents/${agent.AgentId}/modules/collection/files/stream_files_explorer`,
        { path: pathString }
      );

      const newData = response.data;
      // Convert server's RootPath to segments
      const newSegs = pathToSegments(newData.RootPath);

      setPathSegments(newSegs);
      setDirectories(newData.Directories.Items || []);
      setFiles(newData.Files || []);
      // Update the typed path
      setCustomPath(segmentsToPath(newSegs) || "");
      setLoading(false);
    } catch (err) {
      console.error("Failed to fetch explorer:", err);
      setError("Error loading file explorer.");
      setLoading(false);
    }
  }

  function handleGoUp() {
    setPathSegments((prev) => {
      if (prev.length > 0) {
        const next = [...prev];
        next.pop();
        fetchDirectory(next);
        return next;
      }
      return prev; // already root
    });
  }

  function handleRefresh() {
    fetchDirectory(pathSegments);
  }

  function handleApplyPath() {
    const newSegments = pathToSegments(customPath);
    fetchDirectory(newSegments);
  }

  function handleOpenDirectory(dirPath: string) {
    const segs = pathToSegments(dirPath);
    fetchDirectory(segs);
  }

  // Clicking a file => open detail
  function handleOpenFileDetail(file: FileItem) {
    setSelectedFile(file);
  }

  // -- Upload logic --
  function handleUploadClick() {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  }

  /**
   * 1) On file selection, read as base64 using FileReader
   * 2) Strip the "data:...base64," prefix
   * 3) POST { path, file_base64 } to server
   * 4) Refresh listing
   */
  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const reader = new FileReader();
      reader.onload = async (event) => {
        if (!event.target?.result) {
          setError("Failed to read file.");
          setLoading(false);
          return;
        }

        // The result is like "data:application/pdf;base64,JVBERi0xLjQK..."
        const resultStr = event.target.result as string;

        // We want the part after "base64,"
        const base64Index = resultStr.indexOf("base64,");
        if (base64Index === -1) {
          setError("No base64 prefix found.");
          setLoading(false);
          return;
        }
        const base64Data = resultStr.substring(base64Index + 7);

        // POST to server
        const currentPath = segmentsToPath(pathSegments);
        const response = await axiosAuth.post<any>(`/agents/${agent.AgentId}/modules/collection/files/upload_base64`, {
          path: currentPath,
          file_base64: base64Data,
          file_name: file.name
        });
        await getTaskResults(response.data.task_id)

        // Refresh listing
        fetchDirectory(pathSegments);
      };

      reader.onerror = () => {
        setError("Error reading file for upload.");
        setLoading(false);
      };

      reader.readAsDataURL(file);
    } catch (err) {
      console.error("Upload error:", err);
      setError("Upload failed.");
      setLoading(false);
    } finally {
      // Reset input so user can re-pick if desired
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  }

  if (loading) {
    return (
      <div className="card bg-dark text-white" style={{ borderRadius: 16 }}>
        <div className="card-body">
          <div className="d-flex align-items-center gap-2 text-secondary">
            <div className="spinner-border spinner-border-sm" role="status" />
            <span>Loading file explorer...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return <div className="text-danger">{error}</div>;
  }

  const folderIcon = "https://cdn-icons-png.flaticon.com/512/715/715676.png";

  return (
    <>
      <div className="card file-explorer-panel bg-dark text-white d-flex flex-column" style={{ borderRadius: 16 }}>
        <div className="card-header file-explorer-header">
          <div className="row g-2 align-items-center" style={{ width: "100%" }}>
            {/* Left: Up, Refresh, Upload */}
            <div className="col-12 col-sm-auto d-flex gap-2">
              <i className="bi bi-arrow-left" onClick={handleGoUp} style={{ cursor: "pointer" }}></i>
              <button className="btn btn-sm btn-secondary bi bi-arrow-clockwise" onClick={handleRefresh}></button>
              <i
                className="bi bi-upload btn btn-sm btn-secondary"
                style={{ cursor: "pointer" }}
                onClick={handleUploadClick}
              ></i>
              {/* Hidden input for local file selection */}
              <input
                type="file"
                ref={fileInputRef}
                style={{ display: "none" }}
                onChange={handleFileChange}
              />
            </div>

            {/* Right: path input + Go button */}
            <div className="col-12 col-sm d-flex gap-2 path-input-group mt-2">
              <div className="input-group input-group-sm flex-grow-1">
                <input
                  type="text"
                  className="form-control"
                  value={customPath}
                  placeholder="Enter path..."
                  onChange={(e) => setCustomPath(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") handleApplyPath();
                  }}
                />
                <button className="btn btn-primary" onClick={handleApplyPath}>
                  Go
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Directories & files */}
        <div className="flex-grow-1 p-2 overflow-auto file-explorer-body">
          {directories.length > 0 && (
            <div className="mb-3">
              <h6 className="mb-2 text-secondary">Directories</h6>
              <div className="row row-cols-auto g-2">
                {directories.map((dir) => {
                  const folderName = dir.split("\\").pop() || dir;
                  return (
                    <div key={dir} className="col">
                      <div
                        className="file-explorer-item"
                        onClick={() => handleOpenDirectory(dir)}
                        title={folderName}
                      >
                        <img
                          src={folderIcon}
                          alt="Folder"
                          className="file-explorer-icon"
                        />
                        <div className="file-explorer-name text-truncate">{folderName}</div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {files.length > 0 && (
            <div>
              <h6 className="mb-2 text-secondary">Files</h6>
              <div className="row row-cols-auto g-2">
                {files.map((f) => {
                  const fileName = f.Name;
                  return (
                    <div key={f.Path} className="col">
                      <div
                        className="file-explorer-item"
                        onClick={() => handleOpenFileDetail(f)}
                        title={fileName}
                      >
                        {f.Icon && f.Icon !== "Default" ? (
                          <img
                            src={`data:image/png;base64,${f.Icon}`}
                            alt="File Icon"
                            className="file-explorer-icon"
                          />
                        ) : (
                          <svg
                            className="file-explorer-icon"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            fill="white"
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <path d="M6 2H14L20 8V22H6V2Z" stroke="white" strokeWidth="2" />
                          </svg>
                        )}
                        <div className="file-explorer-name text-truncate">{fileName}</div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {directories.length === 0 && files.length === 0 && (
            <p className="text-muted">No directories or files found.</p>
          )}
        </div>
      </div>

      {/* If selectedFile => show detail modal */}
      {selectedFile && (
        <FileDetailModal
          file={selectedFile}
          agentId={agent.AgentId}
          onClose={() => setSelectedFile(null)}
        />
      )}
    </>
  );
}
