# backend/app/mcp_server.py
from typing import Callable, Dict, Any
from .tools.youtube_tool import YouTubeTool

class MCPServer:
    """
    Minimal MCP-like server that registers callable tools and exposes
    an async invoke(interface) method.
    """
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        # register tools
        yt = YouTubeTool()
        self.register_tool("youtube.search", yt.search)
        self.register_tool("youtube.like", yt.like_video)
        self.register_tool("youtube.recommend", yt.get_recommendations_from_likes)

    def register_tool(self, tool_id: str, handler: Callable):
        self.tools[tool_id] = handler

    def list_tools(self):
        return [{"id": k, "doc": getattr(v, "__doc__", "")} for k, v in self.tools.items()]

    def has_tool(self, tool_id: str) -> bool:
        return tool_id in self.tools

    async def invoke(self, tool_id: str, input: Dict[str, Any]) -> Any:
        handler = self.tools[tool_id]
        # handlers are async functions
        return await handler(input)
