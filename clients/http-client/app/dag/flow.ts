import { Node, Edge } from "@xyflow/react";
import { AgentEvent } from "@/hooks/useSocket";
import { AgentNode, buildDag } from "./dag";

const STATUS_COLORS: Record<string, string> = {
    running: "#e168d1",
    success: "#2ee370",
    retry: "#efc444",
    failed: "#ef4444",
    exhausted: "#5b076a",
    end: "#6b7280",
};


function borderColor(status: string): string {
    return STATUS_COLORS[status] ?? "#3f3f46";
}

export function transformDagToFlow(events: AgentEvent[]) {
    const dag = buildDag(events);
    const nodes: Node[] = [];
    const edges: Edge[] = [];

    const levelCounter: Record<number, number> = {};

    function traverse(node: AgentNode, depth: number = 0) {
        if (levelCounter[depth] === undefined) levelCounter[depth] = 0;

        const color = borderColor(node.status);

        nodes.push({
            id: node.agent_id,
            data: {
                label: node.agent.replace(/([a-z])([A-Z])/g, "$1 $2"),
                status: node.status,
            },
            position: {
                x: depth * 300,
                y: levelCounter[depth] * 200,
            },
            style: {
                background: "#18181b",
                color: "#fff",
                border: `2px solid ${color}`,
                borderRadius: "8px",
                width: 220,
            },
        });

        levelCounter[depth]++;

        for (const child of node.children) {
            const done = child.status === "success" || child.status === "end";
            edges.push({
                id: `e-${node.agent_id}-${child.agent_id}`,
                source: node.agent_id,
                target: child.agent_id,
                animated: !done,
                style: { stroke: "#2dd4bf", strokeWidth: 1 },
            });

            traverse(child, depth + 1);
        }
    }

    dag.forEach((root) => traverse(root));

    return { nodes, edges };
}
