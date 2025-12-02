import os
import httpx
import asyncio
import json
from typing import Any, Dict

# --- Environment variables ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Please set it with a valid OpenAI secret key."
    )

SYSTEM_PROMPT = """
You are an MCP-enabled AI agent that interacts with tools exposed by the MCP backend.
You can:
- search YouTube
- like videos
- comment on videos
- subscribe to channels
- fetch liked videos
- provide recommendations based on liked videos

Use JSON format when calling tools:
{
    "tool_calls": [
        {"name": "youtube.search", "arguments": {"q": "query", "max": 5}},
        {"name": "youtube.like_video", "arguments": {"videoId": "...", "token_data": {...}}},
        {"name": "youtube.comment_video", "arguments": {"videoId": "...", "comment_text": "...", "token_data": {...}}},
        {"name": "youtube.subscribe_channel", "arguments": {"channelId": "...", "token_data": {...}}},
        {"name": "youtube.liked_videos", "arguments": {"token_data": {...}, "max": 5}}
    ]
}
"""

# --- OpenAI Chat Model Wrapper ---
async def call_llm(messages):
    import openai
    openai.api_key = OPENAI_API_KEY

    try:
        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
        )
        return response.choices[0].message
    except Exception as e:
        raise RuntimeError(f"OpenAI call failed: {e}") from e

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
            print(f"MCP call failed for {tool_id}: {e}")
            return {"error": str(e)}

# --- Agent Main Function ---
async def run_agent():
    print("Welcome to MCP YouTube AI Agent!")
    print("Commands: search, like, comment, subscribe, liked, exit")

    # Load token_data for OAuth actions
    token_json = input("Enter your OAuth token_data JSON (for like/comment/subscribe/liked actions):\n")
    try:
        token_data = json.loads(token_json)
    except json.JSONDecodeError:
        print("Invalid JSON. Exiting.")
        return

    while True:
        cmd = input("\nEnter command: ").strip().lower()

        if cmd == "exit":
            print("Goodbye!")
            break

        if cmd.startswith("search"):
            query = cmd[len("search"):].strip()
            if not query:
                query = input("Enter search query: ")
            result = await mcp_invoke("youtube.search", {"q": query, "max": 5})
            print(json.dumps(result, indent=2))

        elif cmd.startswith("like"):
            video_id = cmd[len("like"):].strip() or input("Enter video ID to like: ")
            result = await mcp_invoke("youtube.like_video", {"videoId": video_id, "token_data": token_data})
            print(json.dumps(result, indent=2))

        elif cmd.startswith("comment"):
            video_id = input("Enter video ID to comment: ")
            comment_text = input("Enter comment text: ")
            result = await mcp_invoke("youtube.comment_video", {
                "videoId": video_id,
                "comment_text": comment_text,
                "token_data": token_data
            })
            print(json.dumps(result, indent=2))

        elif cmd.startswith("subscribe"):
            channel_id = input("Enter channel ID to subscribe: ")
            result = await mcp_invoke("youtube.subscribe_channel", {"channelId": channel_id, "token_data": token_data})
            print(json.dumps(result, indent=2))

        elif cmd.startswith("liked"):
            max_results = input("Enter max number of liked videos to fetch (default 5): ")
            max_results = int(max_results) if max_results.isdigit() else 5
            result = await mcp_invoke("youtube.liked_videos", {"token_data": token_data, "max": max_results})
            print(json.dumps(result, indent=2))

        else:
            print("Unknown command. Valid commands: search, like, comment, subscribe, liked, exit")

# --- Main Execution ---
if __name__ == "__main__":
    asyncio.run(run_agent())
