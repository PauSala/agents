import { Handle, Position } from "@xyflow/react";
import {
  LucideIcon,
  Bot,
  CheckCircle2,
  AlertCircle,
  Loader2,
} from "lucide-react";

export const ICONS: Record<string, LucideIcon> = {
  running: Loader2,
  success: CheckCircle2,
  failed: AlertCircle,
  end: AlertCircle,
};

const endStatus = (data: Record<string, string>) =>
  data.status === "success" || data.status === "end";

export function AgentNode({ data }: { data: Record<string, string> }) {
  const Icon = ICONS[data.status] || Bot;

  return (
    <div
      className="min-w-[200px] shadow-xl rounded-lg bg-zinc-900 border-1 border-zinc-800 overflow-hidden"
      style={{ borderColor: data.color || "#3f3f46" }}
    >
      {/* Target Handle (Left) */}
      <Handle
        type="target"
        position={Position.Left}
        className="w-3 h-3 bg-teal-500"
      />

      <div className="p-3">
        <div className="flex items-center gap-2 mb-2">
          <div
            className={`p-1.5 rounded-md ${data.status === "running" ? "animate-spin" : ""}`}
          >
            <Icon
              size={16}
              className="text-teal-400"
              style={{ color: data.color || "#3f3f46" }}
            />
          </div>
          <span className="text-xs font-bold uppercase tracking-tight text-zinc-400">
            {data.label}
          </span>
        </div>
      </div>

      {/* Progress Bar at the bottom */}
      <div className="h-1 w-full bg-zinc-800">
        <div
          className={`h-full transition-all duration-500 ${endStatus(data) ? "w-full bg-teal-500" : data.status === "failed" ? "w-full bg-pink-500" : "w-1/3 bg-teal-500/50"}`}
        />
      </div>

      {/* Source Handle (Right) */}
      <Handle
        type="source"
        position={Position.Right}
        className={`w-3 h-3 bg-teal-500`}
      />
    </div>
  );
}
