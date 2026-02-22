import { AgentEvent } from "@/hooks/useSocket";

export interface AgentNode {
    agent: string;
    agent_id: string;
    caller_id: string;
    status: string;
    data: Record<string, string>;
    children: AgentNode[];
}

export function buildDag(events: AgentEvent[]): AgentNode[] {
    const nodesMap = new Map<string, AgentNode>();
    const roots: AgentNode[] = [];

    for (const event of events) {
        const existing = nodesMap.get(event.agent_id);
        if (existing) {
            existing.status = event.status;
            Object.assign(existing.data, event.data);
        } else {
            nodesMap.set(event.agent_id, {
                agent: event.agent,
                agent_id: event.agent_id,
                caller_id: event.caller_id,
                status: event.status,
                data: { ...event.data },
                children: [],
            });
        }
    }

    for (const node of nodesMap.values()) {
        const parent = node.caller_id ? nodesMap.get(node.caller_id) : undefined;
        if (parent) {
            if (!parent.children.some(child => child.agent_id === node.agent_id)) {
                parent.children.push(node);
            }
        } else {
            roots.push(node);
        }
    }

    return roots;
}
