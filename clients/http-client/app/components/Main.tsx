"use client";

import { useState } from "react";
import { useSocket } from "@/hooks/useSocket";
import { StatusHeader } from "@/components/StatusHeader";
import { EventItem } from "@/components/EventItem";

export default function Home() {
  const { events, setEvents, status } = useSocket("ws://localhost:8000/ws");
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.SubmitEvent) => {
    e.preventDefault();
    if (!prompt.trim() || status !== "connected") return;

    setLoading(true);
    setEvents([]);

    try {
      await fetch("http://localhost:8000/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      setPrompt("");
    } catch (error) {
      console.error("Failed to send prompt:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex w-full max-w-3xl flex-col gap-6 bg-white dark:bg-zinc-900 p-8 rounded-xl shadow-sm border border-zinc-200 dark:border-zinc-800">
      <StatusHeader status={status} />

      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <label className="text-sm font-medium dark:text-zinc-300">
          Run a Prompt
        </label>
        <div className="flex gap-2">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={loading || status !== "connected"}
            className="flex-1 px-4 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-sm focus:ring-2 focus:ring-teal-500 disabled:opacity-50"
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

      <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2">
        {events.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-zinc-400">
            <div className="w-8 h-8 mb-2 border-2 border-dashed border-zinc-300 rounded-full animate-spin" />
            <p className="italic text-sm">Waiting for agent activity...</p>
          </div>
        ) : (
          events.map((ev, i) => <EventItem key={i} event={ev} />)
        )}
      </div>
    </main>
  );
}
