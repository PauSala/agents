"use client";

import "@xyflow/react/dist/style.css";
import { transformDagToFlow } from "@/dag/flow";
import { AgentEvent } from "@/hooks/useSocket";
import {
  Background,
  Controls,
  ReactFlow,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
} from "@xyflow/react";
import { useEffect } from "react";
import { AgentNode } from "./AgentNode";

const nodeTypes = {
  agent: AgentNode,
};

export default function AgentGraph({ events }: { events: AgentEvent[] }) {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

  useEffect(() => {
    const { nodes: n, edges: e } = transformDagToFlow(events);
    setNodes(n);
    setEdges(e);
  }, [events, setNodes, setEdges]);

  return (
    <div className="h-[600px] w-full border border-zinc-800 rounded-xl bg-zinc-950">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
        fitView
        colorMode="dark"
        fitViewOptions={{ padding: 2.0 }}
      >
        <Background gap={20} color="#27272a" />
        <Controls />
      </ReactFlow>
    </div>
  );
}
