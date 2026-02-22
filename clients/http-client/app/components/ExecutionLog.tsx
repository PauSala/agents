"use client";
import { AgentEvent } from "@/hooks/useSocket";
import { useEffect, useRef } from "react";
import { EventItem } from "./EventItem";

export function ExecutionLog({
  events,
  isWorking,
}: {
  events: AgentEvent[];
  isWorking: boolean;
}) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new events arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events]);

  return (
    <div className="flex flex-col h-[600px] border border-zinc-800 rounded-xl bg-zinc-950 overflow-hidden shadow-2xl">
      <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800 bg-zinc-900/50 backdrop-blur-md">
        <h3 className="text-xs font-bold uppercase tracking-widest text-zinc-400">
          Execution Log
        </h3>
        {isWorking && (
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-teal-500"></span>
            </span>
            <span className="text-[10px] text-teal-500 font-medium">LIVE</span>
          </div>
        )}
      </div>

      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-zinc-800 scrollbar-track-transparent"
      >
        {events.length === 0 && !isWorking && (
          <div className="h-full flex items-center justify-center text-zinc-600 text-sm italic">
            No activity detected.
          </div>
        )}

        <div className="relative space-y-6">
          {events.length > 1 && (
            <div className="absolute left-[19px] top-2 bottom-2 w-px bg-zinc-800" />
          )}

          {events.map((ev, i) => (
            <div key={i} className="relative z-10">
              <EventItem event={ev} />
            </div>
          ))}
        </div>

        {isWorking && (
          <div className="flex items-start gap-4 py-4 animate-pulse">
            <div className="w-10 h-10 flex items-center justify-center">
              <div className="w-5 h-5 border-2 border-teal-500/30 border-t-teal-500 rounded-full animate-spin" />
            </div>
            <div className="flex-1 space-y-2 mt-1">
              <div className="h-2 w-24 bg-zinc-800 rounded" />
              <div className="h-2 w-full bg-zinc-900 rounded" />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
