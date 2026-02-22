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
  useReactFlow,
} from "@xyflow/react";
import { useEffect } from "react";
import { AgentNode } from "./AgentNode";

const nodeTypes = {
  agent: AgentNode,
};

function FlowUpdater({ nodes }: { nodes: Node[] }) {
  const { fitView } = useReactFlow();

  useEffect(() => {
    if (nodes.length > 0) {
      fitView({
        duration: 300,
        padding: 0.2,
      });
    }
  }, [nodes.length, fitView]);

  return null;
}

export default function AgentGraph({ events }: { events: AgentEvent[] }) {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

  useEffect(() => {
    const { nodes: n, edges: e } = transformDagToFlow(events);
    setNodes(n);
    setEdges(e);
  }, [events, setNodes, setEdges]);

  return (
    <div className="h-[300px] w-full border border-zinc-800 rounded-xl bg-zinc-950">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        maxZoom={1.0}
        nodeTypes={nodeTypes}
        colorMode="dark"
        zoomOnScroll={false}
      >
        <Background gap={20} color="#0f172a" bgColor="#0f172a" />
        <FlowUpdater nodes={nodes} />
        <Controls />
      </ReactFlow>
    </div>
  );
}
