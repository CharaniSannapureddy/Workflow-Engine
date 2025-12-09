from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from typing import Dict, Any
import uuid
import asyncio

import app.storage as storage
from app.engine.graph import Graph, Node
from app.engine.runner import run_graph_async
from app.engine.websocket_manager import manager

import app.workflows.code_review
graphs = storage.graphs
runs = storage.runs

app = FastAPI()

# ---- GRAPH CREATION ----

class GraphCreate(BaseModel):
    nodes: Dict[str, str]
    edges: Dict[str, str]
    start_node: str

@app.post("/graph/create")
def create_graph(req: GraphCreate):
    graph_id = str(uuid.uuid4())
    graphs[graph_id] = Graph(
        id=graph_id,
        nodes={n: Node(name=n, function_name=f) for n, f in req.nodes.items()},
        edges=req.edges,
        start_node=req.start_node
    )
    return {"graph_id": graph_id}


# ---- RUN GRAPH ----

class RunGraphRequest(BaseModel):
    graph_id: str
    state: Dict[str, Any]

@app.post("/graph/run")
async def run_graph(req: RunGraphRequest):
    run_id = str(uuid.uuid4())
    asyncio.create_task(run_graph_async(req.graph_id, req.state, run_id))
    return {"run_id": run_id, "message": "Workflow started."}


# ---- GET STATE ----

@app.get("/graph/state/{run_id}")
def get_state(run_id: str):
    return runs.get(run_id, {"error": "run_id not found"})


# ---- WEBSOCKET LOG STREAM ----

@app.websocket("/ws/logs")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        manager.disconnect(ws)
