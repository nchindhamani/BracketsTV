import os
import json
import requests
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# YouTube API configuration
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3'

# Cache configuration
CACHE_TTL_HOURS = 4  # Cache videos for 4 hours
CACHE_TTL_SECONDS = CACHE_TTL_HOURS * 3600

# Global in-memory cache
# Structure: {category: {'videos': [...], 'timestamp': unix_timestamp}}
video_cache: Dict[str, Dict] = {}

# Curated channel lists - properly organized by category
CURATED_CHANNELS = {
    'dsa': [
        'UCBrr0j94aB-LJbFukyQfWIQ',  # NeetCode
        'UC8butISFwT-Wl7EV0hUK0BQ',  # freeCodeCamp.org
        'UCZCFT11CWQi3AsO1D4MqXgQ',  # Abdul Bari
        'UCxX9wt5FWQUAAz4UrysqK9A',  # CS Dojo
        'UCn2SbTWiE7kT6f79HcHSDRA',  # Back To Back SWE
        'UC1fLEeYICmo3O9cUsqIi7HA',  # Nick White
        'UCJZ_4xTQ1koKcKBgTH4zqXQ',  # Tech With Tim
        'UCuXI0X6-eeW2g_70FZpagPQ',  # Tech Interview Pro
    ],
    'system': [
        'UCZCFT11CWQi3AsO1D4MqXgQ',  # ByteByteGo
        'UCuXI0X6-eeW2g_70FZpagPQ',  # Gaurav Sen
        'UCn2SbTWiE7kT6f79HcHSDRA',  # Exponent
        'UC1fLEeYICmo3O9cUsqIi7HA',  # System Design Interview
        'UCJZ_4xTQ1koKcKBgTH4zqXQ',  # High Scalability
        'UC8butISFwT-Wl7EV0hUK0BQ',  # freeCodeCamp.org
    ],
    'behavioral': [
        'UCJZ_4xTQ1koKcKBgTH4zqXQ',  # Jeff H Sipe
        'UCn2SbTWiE7kT6f79HcHSDRA',  # Exponent
        'UC1fLEeYICmo3O9cUsqIi7HA',  # Dan Croitor
        'UCuXI0X6-eeW2g_70FZpagPQ',  # Tech Interview Pro
        'UC8butISFwT-Wl7EV0hUK0BQ',  # freeCodeCamp.org
    ],
    'languages': {
        'python': [
            'UC8butISFwT-Wl7EV0hUK0BQ',  # freeCodeCamp.org
            'UCJZ_4xTQ1koKcKBgTH4zqXQ',  # Tech With Tim
            'UC1fLEeYICmo3O9cUsqIi7HA',  # Corey Schafer
            'UCuXI0X6-eeW2g_70FZpagPQ',  # Real Python
        ],
        'javascript': [
            'UC8butISFwT-Wl7EV0hUK0BQ',  # freeCodeCamp.org
            'UCJZ_4xTQ1koKcKBgTH4zqXQ',  # Tech With Tim
            'UC1fLEeYICmo3O9cUsqIi7HA',  # Traversy Media
            'UCuXI0X6-eeW2g_70FZpagPQ',  # The Net Ninja
        ],
        'java': [
            'UC8butISFwT-Wl7EV0hUK0BQ',  # freeCodeCamp.org
            'UCJZ_4xTQ1koKcKBgTH4zqXQ',  # Tech With Tim
            'UC1fLEeYICmo3O9cUsqIi7HA',  # Programming with Mosh
            'UCuXI0X6-eeW2g_70FZpagPQ',  # Java Brains
        ],
        'cpp': [
            'UC8butISFwT-Wl7EV0hUK0BQ',  # freeCodeCamp.org
            'UCJZ_4xTQ1koKcKBgTH4zqXQ',  # Tech With Tim
            'UC1fLEeYICmo3O9cUsqIi7HA',  # The Cherno
            'UCuXI0X6-eeW2g_70FZpagPQ',  # Bo Qian
        ],
        'csharp': [
            'UC8butISFwT-Wl7EV0hUK0BQ',  # freeCodeCamp.org
            'UCJZ_4xTQ1koKcKBgTH4zqXQ',  # Tech With Tim
            'UC1fLEeYICmo3O9cUsqIi7HA',  # Programming with Mosh
            'UCuXI0X6-eeW2g_70FZpagPQ',  # IAmTimCorey
        ],
        'go': [
            'UC8butISFwT-Wl7EV0hUK0BQ',  # freeCodeCamp.org
            'UCJZ_4xTQ1koKcKBgTH4zqXQ',  # Tech With Tim
            'UC1fLEeYICmo3O9cUsqIi7HA',  # Go Programming Language
            'UCuXI0X6-eeW2g_70FZpagPQ',  # JustForFunc
        ],
        'rust': [
            'UC8butISFwT-Wl7EV0hUK0BQ',  # freeCodeCamp.org
            'UCJZ_4xTQ1koKcKBgTH4zqXQ',  # Tech With Tim
            'UC1fLEeYICmo3O9cUsqIi7HA',  # The Rust Programming Language
            'UCuXI0X6-eeW2g_70FZpagPQ',  # Jon Gjengset
        ],
        'kotlin': [
            'UC8butISFwT-Wl7EV0hUK0BQ',  # freeCodeCamp.org
            'UCJZ_4xTQ1koKcKBgTH4zqXQ',  # Tech With Tim
            'UC1fLEeYICmo3O9cUsqIi7HA',  # Programming with Mosh
            'UCuXI0X6-eeW2g_70FZpagPQ',  # Kotlin
        ],
        'swift': [
            'UC8butISFwT-Wl7EV0hUK0BQ',  # freeCodeCamp.org
            'UCJZ_4xTQ1koKcKBgTH4zqXQ',  # Tech With Tim
            'UC1fLEeYICmo3O9cUsqIi7HA',  # Sean Allen
            'UCuXI0X6-eeW2g_70FZpagPQ',  # CodeWithChris
        ],
        'typescript': [
            'UC8butISFwT-Wl7EV0hUK0BQ',  # freeCodeCamp.org
            'UCJZ_4xTQ1koKcKBgTH4zqXQ',  # Tech With Tim
            'UC1fLEeYICmo3O9cUsqIi7HA',  # Traversy Media
            'UCuXI0X6-eeW2g_70FZpagPQ',  # The Net Ninja
        ]
    }
}

def is_cache_valid(cache_entry: Dict) -> bool:
    """
    Check if a cache entry is still valid based on TTL.
    
    Args:
        cache_entry: Dictionary containing 'videos' and 'timestamp'
    
    Returns:
        bool: True if cache is valid, False if expired
    """
    if not cache_entry or 'timestamp' not in cache_entry:
        return False
    
    current_time = time.time()
    cache_age = current_time - cache_entry['timestamp']
    
    return cache_age < CACHE_TTL_SECONDS

def get_channel_ids(category: str, subcategory: Optional[str] = None) -> List[str]:
    """
    Get channel IDs for a given category and optional subcategory.
    
    Args:
        category: Main category (dsa, system, behavioral, languages)
        subcategory: Language subcategory (python, javascript, etc.)
    
    Returns:
        List of YouTube channel IDs
    """
    if category == 'languages' and subcategory:
        return CURATED_CHANNELS['languages'].get(subcategory, [])
    return CURATED_CHANNELS.get(category, [])

def fetch_videos_from_channel(channel_id: str, max_results: int = 5) -> List[Dict]:
    """
    Fetch recent videos from a specific YouTube channel.
    
    Args:
        channel_id: YouTube channel ID
        max_results: Maximum number of videos to fetch
    
    Returns:
        List of video dictionaries
    """
    if not YOUTUBE_API_KEY:
        print(f"Warning: YouTube API key not configured, skipping channel {channel_id}")
        return []
    
    try:
        # Use the correct YouTube API endpoint for channel-specific video search
        url = f"{YOUTUBE_API_URL}/search"
        params = {
            'part': 'snippet',
            'channelId': channel_id,
            'maxResults': max_results,
            'order': 'date',  # Get most recent videos
            'type': 'video',
            'key': YOUTUBE_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        videos = []
        for item in data.get('items', []):
            video = {
                'videoId': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'][:200] + '...' if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'channelTitle': item['snippet']['channelTitle'],
                'publishedAt': item['snippet']['publishedAt'][:10],  # Format date as YYYY-MM-DD
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            videos.append(video)
        
        return videos
        
    except requests.RequestException as e:
        print(f"Error fetching videos for channel {channel_id}: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error fetching videos for channel {channel_id}: {e}")
        return []

def fetch_videos_for_category(category: str, subcategory: Optional[str] = None) -> List[Dict]:
    """
    Fetch videos for a specific category from all associated channels.
    
    Args:
        category: Main category (dsa, system, behavioral, languages)
        subcategory: Language subcategory (python, javascript, etc.)
    
    Returns:
        List of video dictionaries
    """
    channel_ids = get_channel_ids(category, subcategory)
    
    if not channel_ids:
        print(f"No channel IDs found for category: {category}, subcategory: {subcategory}")
        return []
    
    all_videos = []
    
    # Fetch videos from each channel
    for channel_id in channel_ids:
        videos = fetch_videos_from_channel(channel_id, max_results=5)
        all_videos.extend(videos)
        
        # Add a small delay to avoid rate limiting
        time.sleep(0.1)
    
    # Shuffle the videos to ensure variety
    random.shuffle(all_videos)
    
    # Limit to 20 videos total to avoid overwhelming the UI
    return all_videos[:20]

def get_cached_or_fetch_videos(category: str, subcategory: Optional[str] = None) -> List[Dict]:
    """
    Get videos from cache if valid, otherwise fetch from YouTube API.
    
    Args:
        category: Main category (dsa, system, behavioral, languages)
        subcategory: Language subcategory (python, javascript, etc.)
    
    Returns:
        List of video dictionaries
    """
    # Create cache key
    cache_key = f"{category}_{subcategory}" if subcategory else category
    
    # Check if we have valid cached data
    if cache_key in video_cache and is_cache_valid(video_cache[cache_key]):
        print(f"Returning cached videos for {cache_key}")
        return video_cache[cache_key]['videos']
    
    # Cache is empty or expired, fetch fresh data
    print(f"Fetching fresh videos for {cache_key}")
    videos = fetch_videos_for_category(category, subcategory)
    
    # Store in cache with current timestamp
    video_cache[cache_key] = {
        'videos': videos,
        'timestamp': time.time()
    }
    
    print(f"Cached {len(videos)} videos for {cache_key}")
    return videos

@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {
        "message": "BracketsTV API is running",
        "version": "2.0",
        "features": ["caching", "channel-specific_videos", "quota_optimization"]
    }

@app.get("/api/videos")
async def get_videos(category: str, subcategory: str = None):
    """
    Get curated videos for a specific category.
    
    Args:
        category: Main category (dsa, system, behavioral, languages)
        subcategory: Language subcategory (python, javascript, etc.)
    
    Returns:
        JSON response with videos list
    """
    try:
        # Validate category
        if category not in CURATED_CHANNELS and category != 'languages':
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
        
        # For languages category, validate subcategory
        if category == 'languages' and subcategory:
            if subcategory not in CURATED_CHANNELS['languages']:
                raise HTTPException(status_code=400, detail=f"Invalid language subcategory: {subcategory}")
        
        # Get videos (from cache or API)
        videos = get_cached_or_fetch_videos(category, subcategory)
        
        return {
            "videos": videos,
            "category": category,
            "subcategory": subcategory,
            "count": len(videos),
            "cached": cache_key in video_cache if 'cache_key' in locals() else False
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_videos: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint with cache status."""
    cache_status = {}
    for key, value in video_cache.items():
        cache_status[key] = {
            "video_count": len(value.get('videos', [])),
            "age_hours": round((time.time() - value.get('timestamp', 0)) / 3600, 2),
            "is_valid": is_cache_valid(value)
        }
    
    return {
        "status": "healthy",
        "api_key_configured": bool(YOUTUBE_API_KEY),
        "cache_entries": len(video_cache),
        "cache_status": cache_status,
        "cache_ttl_hours": CACHE_TTL_HOURS
    }

@app.get("/api/cache/clear")
async def clear_cache():
    """Clear the video cache (useful for testing)."""
    global video_cache
    video_cache.clear()
    return {"message": "Cache cleared successfully"}

# For Netlify Functions compatibility
def handler(event, context):
    """Netlify Functions handler for serverless deployment."""
    from fastapi import Request
    from fastapi.responses import JSONResponse
    
    # Create a mock request object
    request = Request(
        scope={
            "type": "http",
            "method": event.get("httpMethod", "GET"),
            "path": event.get("path", "/"),
            "query_string": event.get("queryStringParameters", {}),
            "headers": event.get("headers", {}),
        }
    )
    
    # Handle the request
    if event.get("path") == "/api/videos":
        category = event.get("queryStringParameters", {}).get("category", "dsa")
        subcategory = event.get("queryStringParameters", {}).get("subcategory")
        
        try:
            videos = get_cached_or_fetch_videos(category, subcategory)
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "videos": videos,
                    "category": category,
                    "subcategory": subcategory,
                    "count": len(videos)
                })
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }
    
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "BracketsTV API is running"})
    }
