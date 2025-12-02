# backend/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
from app.mcp_server import MCPServer

app = FastAPI(title="MCP Server - YouTube Tools")
server = MCPServer()

@app.get("/", tags=["meta"])
def root():
    return {"status": "ok", "mcp": "simple-http"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/tools")
def list_tools():
    """
    List registered MCP tools.
    """
    return server.list_tools()

class InvokeRequest(BaseModel):
    input: Dict[str, Any]

@app.post("/tools/{tool_id}/invoke")
async def invoke_tool(tool_id: str, body: InvokeRequest):
    """
    Invoke a registered tool by id. Body: { "input": { ... } }
    """
    if not server.has_tool(tool_id):
        raise HTTPException(status_code=404, detail="tool not found")
    result = await server.invoke(tool_id, body.input)
    return {"result": result}
