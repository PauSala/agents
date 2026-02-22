import { AgentEvent } from "@/hooks/useSocket";

const formatAgentName = (name: string) =>
  name.replace(/([a-z])([A-Z])/g, "$1 $2");

export const EventItem = ({ event }: { event: AgentEvent }) => {
  const statusStyles =
    {
      running: "bg-purple-500/10 text-purple-500 border-purple-500/20",
      success: "bg-teal-500/10 text-teal-500 border-teal-500/20",
      failed: "bg-red-500/10 text-red-500 border-red-500/20",
      end: "bg-zinc-500/10 text-zinc-400 border-zinc-500/20",
    }[event.status] || "bg-zinc-500/10 text-zinc-400 border-zinc-500/20";
  return (
    <div className="p-4 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-100 dark:border-zinc-700 animate-in fade-in slide-in-from-bottom-2">
      <div className="flex justify-between items-start mb-1">
        <span className="text-xs font-bold uppercase tracking-wider text-teal-600 dark:text-teal-300">
          {formatAgentName(event.agent)}
        </span>
        <span className="text-[12px] text-zinc-400 font-mono">
          {event.timestamp}
        </span>
      </div>
      <p
        className={`flex w-25 justify-center items-center gap-1.5 px-2 py-0.5 rounded-full border text-[10px] font-bold uppercase tracking-tight ${statusStyles}`}
      >
        {event.status}
      </p>
      {event.data && (
        <pre className="mt-3 p-3 bg-black text-green-400 text-xs rounded-md overflow-x-auto font-mono">
          {typeof event.data === "object"
            ? JSON.stringify(event.data, null, 2)
            : event.data}
        </pre>
      )}
    </div>
  );
};
