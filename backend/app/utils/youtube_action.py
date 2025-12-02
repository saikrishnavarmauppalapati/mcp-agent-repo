import os
from typing import Dict, Any, List
import googleapiclient.discovery
from google.oauth2.credentials import Credentials

# --- API Key for public search ---
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


# -----------------------------
# Search Videos (API Key)
# -----------------------------
def search_videos(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    if not YOUTUBE_API_KEY:
        raise RuntimeError("YOUTUBE_API_KEY is not set in environment variables.")

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=YOUTUBE_API_KEY
    )

    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response.get("items", []):
        videos.append({
            "id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "channel": item["snippet"]["channelTitle"],
            "channel_id": item["snippet"]["channelId"]
        })
    return videos


# -----------------------------
# OAuth Client
# -----------------------------
def get_youtube_client(token_data: Dict[str, Any]):
    creds = Credentials(
        token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
        token_uri=token_data.get("token_uri", "https://oauth2.googleapis.com/token"),
    )

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=creds
    )
    return youtube


def like_video(youtube, video_id: str) -> Dict[str, Any]:
    request = youtube.videos().rate(id=video_id, rating="like")
    request.execute()
    return {"status": "success", "videoId": video_id, "action": "liked"}


def comment_video(youtube, video_id: str, comment_text: str) -> Dict[str, Any]:
    comment_body = {
        "snippet": {
            "videoId": video_id,
            "topLevelComment": {"snippet": {"textOriginal": comment_text}}
        }
    }
    request = youtube.commentThreads().insert(
        part="snippet",
        body=comment_body
    )
    response = request.execute()
    return {"status": "success", "comment": response}


def subscribe_channel(youtube, channel_id: str) -> Dict[str, Any]:
    body = {
        "snippet": {
            "resourceId": {
                "kind": "youtube#channel",
                "channelId": channel_id
            }
        }
    }
    request = youtube.subscriptions().insert(
        part="snippet",
        body=body
    )
    response = request.execute()
    return {"status": "success", "subscription": response}


def get_liked_videos(youtube, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch videos liked by the authenticated user.
    """
    request = youtube.videos().list(
        part="snippet,contentDetails",
        myRating="like",
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response.get("items", []):
        videos.append({
            "id": item["id"],
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "channel": item["snippet"]["channelTitle"],
            "channel_id": item["snippet"]["channelId"]
        })
    return videos


def get_recommendations_from_likes(liked_videos: List[Dict[str, Any]]) -> List[str]:
    """
    Mock recommendations based on liked videos.
    """
    recommendations = []
    for vid in liked_videos:
        recommendations.append(f"recommended_for_{vid['id']}")
    return recommendations
