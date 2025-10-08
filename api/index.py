#!/usr/bin/env python3
"""
BracketsTV User-Facing API
==========================

A simple, fast data reader for the Supabase database.
This API serves data to the frontend without making any YouTube API calls.

Endpoints:
    - GET /?type=subcategories&category=<category> - Get subcategories for a category
    - GET /?type=videos&category=<category>&subcategory=<subcategory> - Get videos for a subcategory

Environment Variables Required:
    - SUPABASE_URL: Your Supabase project URL
    - SUPABASE_KEY: Your Supabase service role key (or anon key with proper RLS)
"""

import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="BracketsTV API",
    description="A simple data reader for BracketsTV content",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
try:
    from supabase import create_client, Client
    
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase client initialized successfully")
    
except ImportError:
    print("ERROR: supabase-py not installed. Run: pip install supabase")
    supabase = None
except Exception as e:
    print(f"ERROR: Failed to initialize Supabase client: {e}")
    supabase = None


@app.get("/")
async def get_data(
    type: str = Query(..., description="Type of data to fetch: 'subcategories' or 'videos'"),
    category: Optional[str] = Query(None, description="Category name (e.g., 'dsa', 'system_design')"),
    subcategory: Optional[str] = Query(None, description="Subcategory name (e.g., 'Most Watched', 'Latest Uploads')")
):
    """
    Main API endpoint that handles two types of requests:
    
    1. Get subcategories: /?type=subcategories&category=dsa
    2. Get videos: /?type=videos&category=dsa&subcategory=Most%20Watched
    """
    
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    try:
        if type == "subcategories":
            return await get_subcategories(category)
        elif type == "videos":
            return await get_videos(category, subcategory)
        else:
            raise HTTPException(status_code=400, detail="Invalid type parameter. Use 'subcategories' or 'videos'")
    
    except Exception as e:
        print(f"Error in API endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


async def get_subcategories(category: Optional[str]) -> List[str]:
    """
    Get subcategories for a given category.
    
    Args:
        category: The main category (e.g., 'dsa', 'system_design')
    
    Returns:
        List of subcategory names
    """
    if not category:
        raise HTTPException(status_code=400, detail="Category parameter is required for subcategories")
    
    try:
        # Query subcategories table
        response = supabase.table('subcategories')\
            .select('name')\
            .eq('main_category', category)\
            .eq('is_active', True)\
            .execute()
        
        if not response.data:
            return []
        
        # Extract just the names
        subcategory_names = [row['name'] for row in response.data]
        
        print(f"✅ Found {len(subcategory_names)} subcategories for category '{category}'")
        return subcategory_names
        
    except Exception as e:
        print(f"Error fetching subcategories: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch subcategories: {str(e)}")


async def get_videos(category: Optional[str], subcategory: Optional[str]) -> List[Dict[str, Any]]:
    """
    Get videos for a given category and subcategory.
    
    Args:
        category: The main category (e.g., 'dsa', 'system_design')
        subcategory: The subcategory (e.g., 'Most Watched', 'Latest Uploads')
    
    Returns:
        List of video objects
    """
    if not category:
        raise HTTPException(status_code=400, detail="Category parameter is required for videos")
    
    if not subcategory:
        raise HTTPException(status_code=400, detail="Subcategory parameter is required for videos")
    
    try:
        # Query videos table with dynamic ordering based on subcategory
        query = supabase.table('videos')\
            .select('*')\
            .eq('category', category)\
            .eq('sub_category', subcategory)
        
        # Order by view_count for "Most Watched" subcategories, otherwise by published_at
        if subcategory == "Most Watched":
            query = query.order('view_count', desc=True)
        else:
            query = query.order('published_at', desc=True)
            
        response = query.limit(50).execute()
        
        if not response.data:
            print(f"⚠️  No videos found for category '{category}' and subcategory '{subcategory}'")
            return []
        
        print(f"✅ Found {len(response.data)} videos for '{category}' -> '{subcategory}'")
        return response.data
        
    except Exception as e:
        print(f"Error fetching videos: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch videos: {str(e)}")


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API and database connectivity.
    """
    if not supabase:
        return {"status": "error", "message": "Database connection not available"}
    
    try:
        # Test database connection with a simple query
        response = supabase.table('subcategories').select('count').limit(1).execute()
        return {
            "status": "healthy",
            "message": "API and database are working",
            "database_connected": True
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Database connection failed: {str(e)}",
            "database_connected": False
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)