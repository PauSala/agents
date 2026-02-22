import { useState, useEffect } from "react";

export interface AgentEvent {
  agent: string;
  status: string;
  data: Record<string, string>;
  agent_id: string;
  caller_id: string;
  timestamp: string;
}

export function useSocket(url: string) {
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [status, setStatus] = useState<"connected" | "disconnected">(
    "disconnected",
  );
  const [isWorking, setIsWorking] = useState(false);

  useEffect(() => {
    const socket = new WebSocket(url);

    socket.onopen = () => setStatus("connected");
    socket.onclose = () => setStatus("disconnected");
    socket.onmessage = (event) => {
      try {
        const rawData = JSON.parse(event.data);
        const data =
          typeof rawData === "string" ? JSON.parse(rawData) : rawData;

        console.log(data);
        if (data.status === "end") {
          setIsWorking(false);
        }
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

  return { events, setEvents, status, isWorking, setIsWorking };
}
