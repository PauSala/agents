import { Node, Edge } from "@xyflow/react";
import { AgentEvent } from "@/hooks/useSocket";
import { AgentNode, buildDag } from "./dag";

const STATUS_COLORS: Record<string, string> = {
    running: "#ef7de0",
    success: "#2ee3c2",
    retry: "#efc444",
    failed: "#e26464",
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
    const nodeWidth = 200;

    const xSpacing = nodeWidth + 50;
    const yOffset = 120;
    let xIndex = 0;

    function traverse(node: AgentNode, childIndex: number) {
        const color = borderColor(node.status);

        let y = 0;
        if (xIndex > 0) {
            const direction = childIndex % 2 === 0 ? -1 : 1;
            y = direction * yOffset;
        }

        nodes.push({
            id: node.agent_id,
            type: 'agent',
            data: {
                label: node.agent.replace(/([a-z])([A-Z])/g, "$1 $2"),
                status: node.status,
                color: color
            },
            position: { x: xIndex * xSpacing, y },
        });

        xIndex++;

        node.children.forEach((child, i) => {
            const done = child.status === "success" || child.status === "end";
            edges.push({
                id: `e-${node.agent_id}-${child.agent_id}`,
                source: node.agent_id,
                target: child.agent_id,
                animated: !done,
                style: { stroke: color, strokeWidth: 1 },
                type: '',
            });

            traverse(child, i);
        });
    }

    dag.forEach((root, i) => traverse(root, i));
    return { nodes, edges };
}