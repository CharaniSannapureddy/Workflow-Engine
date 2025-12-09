import uuid
import asyncio
from typing import Dict, Any

from app.storage import graphs, runs
from app.engine.registry import tool_registry
from app.engine.websocket_manager import manager


async def execute_node(fn, state):
    """Run a node function asynchronously."""
    await asyncio.sleep(0)   # free event loop
    return fn(state)


async def run_graph_async(graph_id: str, initial_state: Dict[str, Any], run_id: str):
    graph = graphs[graph_id]
    state = initial_state.copy()
    logs = []

    current = graph.start_node

    while current:
        node = graph.nodes[current]
        fn = tool_registry[node.function_name]

        msg = f"Running node: {current}"
        logs.append(msg)
        await manager.broadcast(msg)

        # async node execution
        state = await execute_node(fn, state)

        msg = f"State after {current}: {state}"
        logs.append(msg)
        await manager.broadcast(msg)

        # branching/looping manually set inside node
        if "__next__" in state:
            current = state["__next__"]
            del state["__next__"]
        else:
            current = graph.edges.get(current)

    runs[run_id] = {"state": state, "logs": logs}
    await manager.broadcast("Workflow finished.")
