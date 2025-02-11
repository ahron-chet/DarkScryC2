"use client";
import { useEffect, useRef, useState } from "react";

interface UseShellWebSocketProps {
    agentId: string;
    accessToken: string;
    onMessage: (msg: string) => void;
}

/**
 * A custom React hook that connects to ws://127.0.0.1:8000/ws/shell/{agentId}/?token=...
 * and handles sending/receiving messages in a shell chat context.
 */
export function useShellWebSocket({
    agentId,
    accessToken,
    onMessage,
}: UseShellWebSocketProps) {
    const [connectionStatus, setConnectionStatus] = useState<"Disconnected" | "Connecting" | "Connected" | "Error">("Disconnected");
    const socketRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        const socketUrl = `ws://127.0.0.1:8000/ws/shell/${agentId}/?token=${accessToken}`;

        setConnectionStatus("Connecting");
        const ws = new WebSocket(socketUrl);
        socketRef.current = ws;

        ws.onopen = () => {
            setConnectionStatus("Connected");
            console.log(`WebSocket open for agent ${agentId}`);
        };
        ws.onmessage = (event) => {
          
            const data = JSON.parse(event.data)
            onMessage(data.message.result.output || "");
        };
        ws.onerror = (err) => {
            console.error("WebSocket error:", err);
            setConnectionStatus("Error");
        };
        ws.onclose = (evt) => {
            console.log("WebSocket closed:", evt.reason);
            setConnectionStatus("Disconnected");
        };

        return () => {
            // cleanup
            if (ws.readyState === WebSocket.OPEN) ws.close();
        };
    }, []);

    // Send text to server
    function sendMessage(text: string) {
        if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
            socketRef.current.send(JSON.stringify({ command: text }));
        }
    }

    return { sendMessage, connectionStatus };
}
