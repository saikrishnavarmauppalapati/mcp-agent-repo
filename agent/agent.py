import os
import httpx
import asyncio
import json
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- Environment variables ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BACKEND_URL = os.getenv("BACKEND_URL", "https://mcp-agent-repo.onrender.com")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Please set it with a valid OpenAI secret key."
    )

# --- FastAPI app ---
app = FastAPI(title="MCP Agent Server")

# Allow CORS for frontend
origins = ["*"]  # Or your frontend URL: ["https://your-frontend-domain.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic model ---
class AgentRequest(BaseModel):
    action: str
    query: str = None
    video_id: str = None
    channel_id: str = None
    comment_text: str = None
    token_data: Dict[str, Any] = None
    max_results: int = 5

# --- MCP Tool Call Helper ---
async def mcp_invoke(tool_id: str, input: Dict[str, Any]):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(
                f"{BACKEND_URL}/tools/{tool_id}/invoke",
                json={"input": input},
                timeout=20.0,
            )
            res.raise_for_status()
            return res.json()["result"]
        except Exception as e:
            return {"error": f"MCP call failed for {tool_id}: {str(e)}"}

# --- Agent HTTP endpoint ---
@app.post("/agent")
async def run_agent(request: AgentRequest):
    action = request.action.lower()

    if action == "search":
        if not request.query:
            raise HTTPException(status_code=400, detail="Query is required for search")
        return await mcp_invoke("youtube.search", {"q": request.query, "max": request.max_results})

    elif action == "like":
        if not request.video_id or not request.token_data:
            raise HTTPException(status_code=400, detail="video_id and token_data required for like")
        return await mcp_invoke("youtube.like", {"videoId": request.video_id, "token_data": request.token_data})

    elif action == "comment":
        if not request.video_id or not request.comment_text or not request.token_data:
            raise HTTPException(status_code=400, detail="video_id, comment_text and token_data required for comment")
        return await mcp_invoke("youtube.comment", {
            "videoId": request.video_id,
            "comment_text": request.comment_text,
            "token_data": request.token_data
        })

    elif action == "subscribe":
        if not request.channel_id or not request.token_data:
            raise HTTPException(status_code=400, detail="channel_id and token_data required for subscribe")
        return await mcp_invoke("youtube.subscribe", {"channelId": request.channel_id, "token_data": request.token_data})

    elif action == "liked":
        if not request.token_data:
            raise HTTPException(status_code=400, detail="token_data required for liked videos")
        return await mcp_invoke("youtube.recommend", {"token_data": request.token_data, "max": request.max_results})

    else:
        raise HTTPException(status_code=400, detail="Unknown action")

# --- Main ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
