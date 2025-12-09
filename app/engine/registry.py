tool_registry = {}

def register_tool(name: str, fn):
    tool_registry[name] = fn
