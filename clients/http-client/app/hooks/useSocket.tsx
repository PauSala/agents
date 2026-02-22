import { useState, useEffect } from "react";

export interface AgentEvent {
  agent?: string;
  status?: string;
  data?: Record<string, string>;
  timestamp?: string;
}

export function useSocket(url: string) {
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [status, setStatus] = useState<"connected" | "disconnected">(
    "disconnected",
  );

  useEffect(() => {
    const socket = new WebSocket(url);

    socket.onopen = () => setStatus("connected");
    socket.onclose = () => setStatus("disconnected");
    socket.onmessage = (event) => {
      try {
        const rawData = JSON.parse(event.data);
        const data =
          typeof rawData === "string" ? JSON.parse(rawData) : rawData;
        setEvents((prev) => [
          ...prev,
          { ...data, timestamp: new Date().toLocaleTimeString() },
        ]);
      } catch (err) {
        console.error("Socket parse error:", err);
      }
    };

    return () => socket.close();
  }, [url]);

  return { events, setEvents, status };
}
