# **README.md**
---

#  **Minimal Agent Workflow Engine**

This project implements a **minimal agent workflow engine** inspired by LangGraph.
The system allows defining a workflow as a set of nodes, edges, shared state, and optional loops or branching.
Workflows are executed through **FastAPI endpoints**, with real-time log streaming supported via **WebSockets**.

---

# **1. Features Implemented**

###  **Workflow / Graph Engine**

* Node = Python function
* Shared state flows between nodes
* Directed edges define execution order
* Conditional branching support
* Loop support (execute until a condition is met)
* Execution logs stored for state review

### **Tool Registry**

* Simple dictionary-based function registry
* Nodes call tools using function names
* Tools for:

  * Extracting functions from code
  * Checking complexity
  * Detecting issues
  * Suggesting improvements

### **FastAPI Endpoints**

| Method | Route                   | Description                           |
| ------ | ----------------------- | ------------------------------------- |
| POST   | `/graph/create`         | Create a workflow graph               |
| POST   | `/graph/run`            | Execute a graph asynchronously        |
| GET    | `/graph/state/{run_id}` | Retrieve state/logs of a workflow run |
| WS     | `/ws/logs`              | Real-time log streaming               |

### **Asynchronous Graph Execution**

* Each run executes in the background
* User receives `run_id` immediately
* State can be checked anytime through API

### **In-Memory Storage**

* Graphs and runs stored in `storage.py`
* No external DB required

---

#   **2. Project Structure**

```
Project-Folder/
│
├── app/
│   ├── main.py                 
│   ├── storage.py              
│   │
│   ├── engine/
│   │   ├── graph.py           
│   │   ├── runner.py           
│   │   ├── websocket_manager.py
│   │
│   ├── workflows/
│       ├── code_review.py      
│
├── README.md
```

---

#  **3. How to Run the Project**

### **Step 1 — Install dependencies**

```
pip install fastapi uvicorn
```

### **Step 2 — Start the FastAPI server**

```
uvicorn app.main:app --reload
```

Server runs at:

👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

API documentation:

👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

# **4. API Usage**


##  **Create a Graph**

**POST /graph/create**

**Request:**

```json
{
  "nodes": {
    "extract": "extract_functions",
    "complexity": "check_complexity",
    "detect": "detect_issues",
    "improve": "suggest_improvements"
  },
  "edges": {
    "extract": "complexity",
    "complexity": "detect",
    "detect": "improve"
  },
  "start_node": "extract"
}
```

**Response:**

```json
{
  "graph_id": "generated-uuid"
}
```

---

##  **Run a Graph**

**POST /graph/run**

```json
{
  "graph_id": "your-graph-id",
  "state": {
    "code": "def a(): pass\ndef b(): pass",
    "quality_score": 1,
    "threshold": 7
  }
}
```

**Response:**

```json
{
  "run_id": "run-uuid",
  "message": "Workflow started."
}
```

---

##  **Get State**

**GET /graph/state/{run_id}**

Returns:

* current shared state
* execution logs
* loop status

---

##  **WebSocket Logs**

Tools like Chrome WebSocket Client can connect to:

```
ws://127.0.0.1:8000/ws/logs
```

You will receive real-time execution logs.

---




