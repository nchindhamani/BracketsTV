#!/usr/bin/env python3
"""
BracketsTV Video Ingestion Script
==================================

This script reads configuration from Supabase, fetches video data from the 
YouTube Data API, and saves the results back to the database.

It's designed to run as a scheduled background job (e.g., via cron or a 
task scheduler) to keep the video database fresh and up-to-date.

Tables:
    - Read from: channels, subcategories, subcategory_channels
    - Write to: videos

Environment Variables Required:
    - YOUTUBE_API_KEY: Your YouTube Data API v3 key
    - SUPABASE_URL: Your Supabase project URL
    - SUPABASE_KEY: Your Supabase service role key (or anon key with proper RLS)
"""

import os
import sys
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("ERROR: google-api-python-client not installed.")
    print("Install with: pip install google-api-python-client")
    sys.exit(1)

try:
    from supabase import create_client, Client
except ImportError:
    print("ERROR: supabase-py not installed.")
    print("Install with: pip install supabase")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configuration
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# TEMPORARY TESTING FLAG - Set to None to process all, or a number to limit
TEST_LIMIT = 3  # Only process first 3 subcategories for testing

# Validate environment variables
if not YOUTUBE_API_KEY:
    print("ERROR: YOUTUBE_API_KEY not found in environment variables")
    sys.exit(1)

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    sys.exit(1)

# Initialize clients
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting BracketsTV Video Ingestion")
print(f"Supabase URL: {SUPABASE_URL}")
print(f"YouTube API Key: {'*' * (len(YOUTUBE_API_KEY) - 4)}{YOUTUBE_API_KEY[-4:]}")
print("-" * 80)


def get_all_subcategories() -> List[Dict[str, Any]]:
    """
    Fetch all active subcategories from the database.
    
    Returns:
        List of subcategory dictionaries with columns: id, name, category, 
        strategy, search_query, order_param, video_duration, max_results
    """
    try:
        print("\n📋 Fetching active subcategories from database...")
        response = supabase.table('subcategories').select('*').eq('is_active', True).execute()
        
        subcategories = response.data
        print(f"   ✓ Found {len(subcategories)} active subcategories to process")
        return subcategories
        
    except Exception as e:
        print(f"   ✗ ERROR fetching subcategories: {e}")
        return []


def get_channel_handles_for_subcategory(subcategory_id: int) -> List[str]:
    """
    Get the list of active YouTube channel handles associated with a subcategory.
    
    Args:
        subcategory_id: The ID of the subcategory
        
    Returns:
        List of channel handles (e.g., ['@NeetCode', '@freeCodeCamp'])
    """
    try:
        # Join subcategory_channels and channels tables, filter for active channels only
        response = supabase.table('subcategory_channels') \
            .select('channels!inner(channel_handle, is_active)') \
            .eq('subcategory_id', subcategory_id) \
            .eq('channels.is_active', True) \
            .execute()
        
        # Extract channel handles from nested structure
        handles = [item['channels']['channel_handle'] for item in response.data if item.get('channels')]
        
        if handles:
            print(f"   → Using {len(handles)} active curated channels: {', '.join(handles[:3])}{'...' if len(handles) > 3 else ''}")
        
        return handles
        
    except Exception as e:
        print(f"   ✗ ERROR fetching channel handles: {e}")
        return []


def search_youtube_videos(query: str, order: str = 'relevance', 
                         video_duration: Optional[str] = None, 
                         max_results: int = 20) -> List[str]:
    """
    Search YouTube and return a list of video IDs.
    
    Args:
        query: Search query string
        order: Sort order (relevance, date, rating, viewCount, title)
        video_duration: Video duration filter (short, medium, long, any)
        max_results: Maximum number of results to return
        
    Returns:
        List of video IDs
    """
    try:
        print(f"   → Searching YouTube: query='{query[:60]}...', order={order}, duration={video_duration}")
        
        search_params = {
            'part': 'id',
            'q': query,
            'type': 'video',
            'maxResults': max_results,
            'order': order,
            'relevanceLanguage': 'en'
        }
        
        if video_duration:
            search_params['videoDuration'] = video_duration
        
        response = youtube.search().list(**search_params).execute()
        
        video_ids = [item['id']['videoId'] for item in response.get('items', [])]
        print(f"   ✓ Found {len(video_ids)} videos")
        
        return video_ids
        
    except HttpError as e:
        print(f"   ✗ YouTube API Error: {e.resp.status} - {e.error_details}")
        
        # Check for quota exceeded error
        if e.resp.status == 403:
            error_reason = e.error_details[0].get('reason', '') if e.error_details else ''
            if 'quota' in error_reason.lower():
                print("   ⚠ YouTube API quota exceeded. Waiting until tomorrow or request quota increase.")
        
        return []
        
    except Exception as e:
        print(f"   ✗ ERROR searching YouTube: {e}")
        return []


def get_video_details(video_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch full details for a list of video IDs using the videos.list endpoint.
    
    This is a more efficient API call that retrieves comprehensive metadata
    including statistics, content details, and full descriptions.
    
    Args:
        video_ids: List of YouTube video IDs
        
    Returns:
        List of video detail dictionaries
    """
    if not video_ids:
        return []
    
    try:
        print(f"   → Fetching full details for {len(video_ids)} videos...")
        
        # YouTube API allows up to 50 IDs per request
        all_videos = []
        
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            
            response = youtube.videos().list(
                part='snippet',  # Only need snippet, not statistics or contentDetails
                id=','.join(batch)
            ).execute()
            
            all_videos.extend(response.get('items', []))
            
            # Rate limiting: small delay between batches
            if i + 50 < len(video_ids):
                time.sleep(0.2)
        
        print(f"   ✓ Retrieved details for {len(all_videos)} videos")
        return all_videos
        
    except HttpError as e:
        print(f"   ✗ YouTube API Error fetching details: {e.resp.status} - {e.error_details}")
        return []
        
    except Exception as e:
        print(f"   ✗ ERROR fetching video details: {e}")
        return []


def parse_duration_to_seconds(duration: str) -> int:
    """
    Parse YouTube ISO 8601 duration to seconds.
    
    Example: 'PT15M33S' -> 933 seconds
    
    Args:
        duration: ISO 8601 duration string
        
    Returns:
        Duration in seconds
    """
    import re
    
    pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, duration)
    
    if not match:
        return 0
    
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    
    return hours * 3600 + minutes * 60 + seconds


def format_video_for_database(video: Dict[str, Any], subcategory_id: int, category: str, subcategory: str) -> Dict[str, Any]:
    """
    Format a YouTube video object into a dictionary matching our videos table schema.
    
    Args:
        video: YouTube video resource from videos.list()
        subcategory_id: The subcategory this video belongs to (not currently used by schema)
        category: Main category (e.g., 'dsa', 'system_design') - NOT NULL in DB
        subcategory: Subcategory name (e.g., 'Most Watched')
        
    Returns:
        Dictionary ready for database insertion
    """
    snippet = video.get('snippet', {})
    
    return {
        'video_id': video['id'],
        'category': category,  # NOT NULL - required!
        'subcategory': subcategory,
        'title': snippet.get('title', 'Untitled'),
        'description': snippet.get('description', '')[:500],  # Truncate to 500 chars
        'channel_title': snippet.get('channelTitle', 'Unknown Channel'),  # NOT NULL - required!
        'published_at': snippet.get('publishedAt'),
        'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', '')
    }


def save_videos_to_database(videos: List[Dict[str, Any]]) -> int:
    """
    Save or update videos in the database using upsert.
    
    Args:
        videos: List of formatted video dictionaries
        
    Returns:
        Number of videos successfully saved
    """
    if not videos:
        return 0
    
    try:
        print(f"   → Saving {len(videos)} videos to database...")
        
        # Upsert will insert new records and update existing ones based on video_id
        response = supabase.table('videos').upsert(
            videos,
            on_conflict='video_id'
        ).execute()
        
        saved_count = len(response.data) if response.data else 0
        print(f"   ✓ Successfully saved/updated {saved_count} videos")
        
        return saved_count
        
    except Exception as e:
        print(f"   ✗ ERROR saving videos to database: {e}")
        return 0


def process_subcategory(subcategory: Dict[str, Any]) -> int:
    """
    Process a single subcategory: fetch videos and save to database.
    
    Args:
        subcategory: Subcategory dictionary from database
        
    Returns:
        Number of videos successfully processed
    """
    subcat_id = subcategory['id']
    subcat_name = subcategory['name']
    category = subcategory['main_category']
    strategy = subcategory['strategy']
    search_query = subcategory.get('search_query', '')
    order_param = subcategory.get('order_param', 'relevance')
    video_duration = subcategory.get('video_duration')
    max_results = subcategory.get('max_results', 20)
    
    print(f"\n{'='*80}")
    print(f"Processing: {category} → {subcat_name}")
    print(f"Strategy: {strategy}")
    print(f"{'='*80}")
    
    video_ids = []
    
    # Execute fetching strategy based on strategy type
    if strategy == 'TOPIC_CURATED':
        # Fetch videos from curated channels with targeted search
        channel_handles = get_channel_handles_for_subcategory(subcat_id)
        
        if not channel_handles:
            print("   ⚠ No curated channels found for this subcategory, skipping...")
            return 0
        
        # Build query: combine search_query with channel handles
        # Example: "(trees OR graphs) AND (@NeetCode OR @freeCodeCamp)"
        channel_part = ' OR '.join(channel_handles)
        combined_query = f"{search_query} AND ({channel_part})"
        
        video_ids = search_youtube_videos(
            query=combined_query,
            order='relevance',
            max_results=max_results
        )
        
    elif strategy == 'POPULARITY':
        # Search across all of YouTube by popularity metric
        video_ids = search_youtube_videos(
            query=search_query,
            order=order_param,  # 'viewCount' or 'rating'
            max_results=max_results
        )
        
    elif strategy == 'RECENCY':
        # Search by recency (latest uploads)
        video_ids = search_youtube_videos(
            query=search_query,
            order='date',
            max_results=max_results
        )
        
    elif strategy == 'FORMAT_DURATION':
        # Filter by video duration
        video_ids = search_youtube_videos(
            query=search_query,
            order='relevance',
            video_duration=video_duration,  # 'short', 'medium', 'long'
            max_results=max_results
        )
        
    elif strategy == 'RECENCY_CURATED':
        # Fetch latest uploads from curated channels
        channel_handles = get_channel_handles_for_subcategory(subcat_id)
        
        if not channel_handles:
            print("   ⚠ No curated channels found for this subcategory, skipping...")
            return 0
        
        # Build query with channel handles, ordered by date
        channel_part = ' OR '.join(channel_handles)
        combined_query = f"{search_query} AND ({channel_part})" if search_query else f"({channel_part})"
        
        video_ids = search_youtube_videos(
            query=combined_query,
            order='date',
            max_results=max_results
        )
        
    elif strategy == 'FORMAT_KEYWORD':
        # Search for videos matching specific keywords (like "masterclass", "complete guide", etc.)
        video_ids = search_youtube_videos(
            query=search_query,
            order='relevance',
            max_results=max_results
        )
        
    else:
        print(f"   ⚠ Unknown strategy '{strategy}', skipping...")
        return 0
    
    # If no videos found, return early
    if not video_ids:
        print("   ℹ No videos found for this subcategory")
        return 0
    
    # Fetch full video details
    video_details = get_video_details(video_ids)
    
    if not video_details:
        print("   ℹ No video details retrieved")
        return 0
    
    # Format videos for database
    formatted_videos = [
        format_video_for_database(video, subcat_id, category, subcat_name) 
        for video in video_details
    ]
    
    # Save to database
    saved_count = save_videos_to_database(formatted_videos)
    
    return saved_count


def main():
    """
    Main execution function: orchestrates the entire ingestion process.
    """
    start_time = time.time()
    total_videos_saved = 0
    
    try:
        # Step 1: Fetch all subcategories from database
        subcategories = get_all_subcategories()
        
        if not subcategories:
            print("\n⚠ No subcategories found in database. Exiting.")
            return
        
        # Step 2: Process each subcategory (with optional test limit)
        subcategories_to_process = subcategories[:TEST_LIMIT] if TEST_LIMIT else subcategories
        total_subcategories = len(subcategories)
        limit_message = f" (TESTING: limited to first {TEST_LIMIT})" if TEST_LIMIT else ""
        
        print(f"\n📊 Processing {len(subcategories_to_process)}/{total_subcategories} subcategories{limit_message}")
        
        for idx, subcategory in enumerate(subcategories_to_process, 1):
            print(f"\n[{idx}/{len(subcategories_to_process)}]", end=' ')
            
            try:
                videos_saved = process_subcategory(subcategory)
                total_videos_saved += videos_saved
                
                # Rate limiting: sleep between subcategories to avoid API throttling
                if idx < len(subcategories_to_process):
                    time.sleep(1)
                    
            except Exception as e:
                print(f"\n   ✗ ERROR processing subcategory: {e}")
                continue
        
        # Summary
        elapsed_time = time.time() - start_time
        print("\n" + "="*80)
        print(f"✅ Ingestion Complete!")
        print(f"   • Processed: {len(subcategories)} subcategories")
        print(f"   • Total videos saved/updated: {total_videos_saved}")
        print(f"   • Time elapsed: {elapsed_time:.2f} seconds")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Ingestion interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n\n✗ FATAL ERROR: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

