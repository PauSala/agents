export const StatusHeader = ({ status }: { status: string }) => (
  <header className="flex justify-between items-center border-b border-zinc-100 dark:border-zinc-800 pb-4">
    <div>
      <h1 className="text-xl font-bold dark:text-white">Agent Pipeline</h1>
      <p className="text-xs text-zinc-500">Real-time LLM Orchestration</p>
    </div>
    <span
      className={`px-2 py-1 rounded text-[10px] font-bold ${status === "connected" ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}
    >
      {status.toUpperCase()}
    </span>
  </header>
);
