"use client";

import "@xyflow/react/dist/style.css";
import { transformDagToFlow } from "@/dag/flow";
import { AgentEvent } from "@/hooks/useSocket";
import { Background, Controls, ReactFlow } from "@xyflow/react";
import { useMemo } from "react";

export default function AgentGraph({ events }: { events: AgentEvent[] }) {
  const { nodes, edges } = useMemo(() => transformDagToFlow(events), [events]);

  return (
    <div className="h-[600px] w-full border border-zinc-800 rounded-xl bg-zinc-950">
      <ReactFlow nodes={nodes} edges={edges} fitView colorMode="dark">
        <Background gap={20} color="#27272a" />
        <Controls />
      </ReactFlow>
    </div>
  );
}
