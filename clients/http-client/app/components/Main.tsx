"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [events, setEvents] = useState<Record<string, string>[]>([]);
  const [status, setStatus] = useState("disconnected");
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws");
    socket.onopen = () => setStatus("connected");
    socket.onclose = () => setStatus("disconnected");
    socket.onmessage = (event) => {
      const rawData = JSON.parse(event.data);
      const data = typeof rawData === "string" ? JSON.parse(rawData) : rawData;
      console.log(data);
      setEvents((prev) => [...prev, data]);
    };
    return () => socket.close();
  }, []);

  const handleSubmit = async (e: React.SubmitEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setLoading(true);
    setEvents([]);

    try {
      const response = await fetch("http://localhost:8000/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (response.ok) {
        setPrompt("");
      }
    } catch (error) {
      console.error("Failed to send prompt:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex w-full max-w-3xl flex-col gap-6 bg-white dark:bg-zinc-900 p-8 rounded-xl shadow-sm border border-zinc-200 dark:border-zinc-800">
      <header className="flex justify-between items-center border-b border-zinc-100 dark:border-zinc-800 pb-4">
        <div>
          <h1 className="text-xl font-bold dark:text-white">Agent Pipeline</h1>
          <p className="text-xs text-zinc-500">Real-time LLM Orchestration</p>
        </div>
        <span
          className={`px-2 m-2 py-1 rounded text-[10px] font-bold ${status === "connected" ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}
        >
          {status.toUpperCase()}
        </span>
      </header>

      {/* --- Input Form --- */}
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <label className="text-sm font-medium dark:text-zinc-300">
          Run a Prompt
        </label>
        <div className="flex gap-2">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g. Solve x^2 + 5x + 6 = 0"
            disabled={loading || status !== "connected"}
            className="flex-1 px-4 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={loading || status !== "connected"}
            className="px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
          >
            {loading ? "Sending..." : "Run"}
          </button>
        </div>
      </form>

      <hr className="border-zinc-100 dark:border-zinc-800" />

      {/* --- Events List --- */}
      <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2">
        {events.length === 0 && (
          <div className="flex flex-col items-center justify-center py-12 text-zinc-400">
            <div className="w-8 h-8 mb-2 border-2 border-dashed border-zinc-300 rounded-full animate-spin" />
            <p className="italic text-sm">Waiting for agent activity...</p>
          </div>
        )}

        {events.map((ev, i) => (
          <div
            key={i}
            className="p-4 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-100 dark:border-zinc-700 animate-in fade-in slide-in-from-bottom-2"
          >
            <div className="flex justify-between items-start mb-1">
              <span className="text-xs font-bold uppercase tracking-wider text-teal-600 dark:text-teal-300">
                {ev.agent || "System"}
              </span>
              <span className="text-[12px] text-zinc-200 font-mono">
                {new Date().toLocaleTimeString()}
              </span>
            </div>
            <p className="text-sm text-zinc-800 dark:text-zinc-200">
              {ev.status || "Processing..."}
            </p>
            {ev.data && (
              <pre className="mt-3 p-3 bg-black text-green-400 text-xs rounded-md overflow-x-auto font-mono">
                {typeof ev.data === "object"
                  ? JSON.stringify(ev.data, null, 2)
                  : ev.data}
              </pre>
            )}
          </div>
        ))}
      </div>
    </main>
  );
}
