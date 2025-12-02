import asyncio
from typing import Dict, Any
from app.utils.youtube_action import (
    search_videos, get_youtube_client, like_video as yt_like,
    comment_video as yt_comment, subscribe_channel as yt_subscribe,
    get_liked_videos, get_recommendations_from_likes
)


class YouTubeTool:

    def __init__(self):
        pass

    async def search(self, input: Dict[str, Any]):
        q = input.get("q", "")
        max_results = int(input.get("max", 5))
        return search_videos(q, max_results)

    async def like_video(self, input: Dict[str, Any]):
        video_id = input.get("videoId")
        token_data = input.get("token_data")
        if not video_id or not token_data:
            return {"ok": False, "error": "missing videoId or token_data"}
        youtube = get_youtube_client(token_data)
        return yt_like(youtube, video_id)

    async def comment_video(self, input: Dict[str, Any]):
        video_id = input.get("videoId")
        comment_text = input.get("comment_text", "")
        token_data = input.get("token_data")
        if not video_id or not token_data or not comment_text:
            return {"ok": False, "error": "missing parameters"}
        youtube = get_youtube_client(token_data)
        return yt_comment(youtube, video_id, comment_text)

    async def subscribe_channel(self, input: Dict[str, Any]):
        channel_id = input.get("channelId")
        token_data = input.get("token_data")
        if not channel_id or not token_data:
            return {"ok": False, "error": "missing parameters"}
        youtube = get_youtube_client(token_data)
        return yt_subscribe(youtube, channel_id)

    async def liked_videos(self, input: Dict[str, Any]):
        token_data = input.get("token_data")
        max_results = int(input.get("max", 10))
        if not token_data:
            return {"ok": False, "error": "missing token_data"}
        youtube = get_youtube_client(token_data)
        liked = get_liked_videos(youtube, max_results)
        recommendations = get_recommendations_from_likes(liked)
        return {"liked_videos": liked, "recommendations": recommendations}
	
    async def get_recommendations_from_likes(self, input: Dict[str, Any]):
    	liked = input.get("liked_videos", [])
    	if not liked:
            return {"ok": False, "error": "No liked videos provided"}
    	recommendations = get_recommendations_from_likes(liked)
    	return {"recommendations": recommendations}

