from pydantic import BaseModel
from typing import Dict

class Node(BaseModel):
    name: str
    function_name: str

class Graph(BaseModel):
    id: str
    nodes: Dict[str, Node]
    edges: Dict[str, str]
    start_node: str
