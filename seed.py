#!/usr/bin/env python3
"""
BracketsTV Database Seeding Script
===================================

This script populates the Supabase configuration tables (channels, subcategories, 
subcategory_channels) with the initial "source of truth" data for the BracketsTV 
application.

The script is idempotent - it can be run multiple times safely using upsert operations.

Configuration Data Source:
    - All channel and subcategory data is imported from config_data.py
    - MASTER_CHANNEL_LIST: Contains all YouTube channel definitions
    - APP_CONFIG: Contains all category and subcategory configurations
    
    Note: To update channels or subcategories, edit config_data.py

Tables Populated:
    - channels: All YouTube channels used in the app
    - subcategories: All content subcategories with their fetching strategies
    - subcategory_channels: Relationships between subcategories and channels

Environment Variables Required:
    - SUPABASE_URL: Your Supabase project URL
    - SUPABASE_KEY: Your Supabase service role key (or anon key with proper RLS)
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dotenv import load_dotenv

# Import configuration data from config_data.py
# This file contains MASTER_CHANNEL_LIST and APP_CONFIG
from config_data import MASTER_CHANNEL_LIST, APP_CONFIG

try:
    from supabase import create_client, Client
except ImportError:
    print("ERROR: supabase-py not installed.")
    print("Install with: pip install supabase")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Validate environment variables
if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    sys.exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting BracketsTV Database Seeding")
print(f"Supabase URL: {SUPABASE_URL}")
print("=" * 80)


def seed_channels():
    """
    Seed the channels table with all YouTube channels from MASTER_CHANNEL_LIST.
    Uses upsert to handle duplicates based on channel_id.
    """
    print("\n📺 Seeding channels table...")
    
    try:
        # Prepare channel data for database
        channels_data = []
        for channel_name, channel_info in MASTER_CHANNEL_LIST.items():
            channels_data.append({
                'name': channel_name,
                'channel_id': channel_info['channel_id'],
                'handle': channel_info['channel_handle'],
                'is_active': True  # All channels active by default
            })
        
        # Upsert channels (insert or update on conflict)
        response = supabase.table('channels').upsert(
            channels_data,
            on_conflict='channel_id'
        ).execute()
        
        print(f"   ✓ Successfully seeded {len(channels_data)} channels")
        return True
        
    except Exception as e:
        print(f"   ✗ ERROR seeding channels: {e}")
        return False


def seed_subcategories():
    """
    Seed the subcategories table with all subcategories from APP_CONFIG.
    Uses upsert to handle duplicates based on (category, name).
    """
    print("\n📁 Seeding subcategories table...")
    
    try:
        # Prepare subcategory data for database
        subcategories_data = []
        for category_config in APP_CONFIG:
            main_category = category_config['main_category']
            
            for subcat in category_config['subcategories']:
                subcategories_data.append({
                    'category': main_category,
                    'name': subcat['name'],
                    'strategy': subcat['strategy'],
                    'search_query': subcat.get('search_query', ''),
                    'order_param': subcat.get('order_param'),
                    'video_duration': subcat.get('video_duration'),
                    'max_results': subcat.get('max_results', 20),
                    'is_active': subcat.get('is_active', True)
                })
        
        # Upsert subcategories
        # Note: Supabase upsert requires a unique constraint. 
        # Assuming you have a unique constraint on (category, name)
        response = supabase.table('subcategories').upsert(
            subcategories_data,
            on_conflict='category,name'
        ).execute()
        
        print(f"   ✓ Successfully seeded {len(subcategories_data)} subcategories")
        return True
        
    except Exception as e:
        print(f"   ✗ ERROR seeding subcategories: {e}")
        return False


def seed_links():
    """
    Seed the subcategory_channels junction table to create relationships
    between subcategories and their associated channels.
    """
    print("\n🔗 Seeding subcategory_channels relationships...")
    
    try:
        # Step 1: Fetch all channels to create name -> id mapping
        print("   → Fetching channels from database...")
        channels_response = supabase.table('channels').select('id, name').execute()
        channel_map = {ch['name']: ch['id'] for ch in channels_response.data}
        print(f"   ✓ Loaded {len(channel_map)} channels")
        
        # Step 2: Fetch all subcategories to create (category, name) -> id mapping
        print("   → Fetching subcategories from database...")
        subcats_response = supabase.table('subcategories').select('id, category, name').execute()
        subcat_map = {(sc['category'], sc['name']): sc['id'] for sc in subcats_response.data}
        print(f"   ✓ Loaded {len(subcat_map)} subcategories")
        
        # Step 3: Build relationships
        print("   → Building relationships...")
        links_data = []
        
        for category_config in APP_CONFIG:
            main_category = category_config['main_category']
            
            for subcat in category_config['subcategories']:
                subcat_name = subcat['name']
                channel_names = subcat.get('channels', [])
                
                # Get subcategory ID
                subcat_key = (main_category, subcat_name)
                if subcat_key not in subcat_map:
                    print(f"   ⚠ Warning: Subcategory not found: {subcat_key}")
                    continue
                
                subcat_id = subcat_map[subcat_key]
                
                # Create link for each channel
                for channel_name in channel_names:
                    if channel_name not in channel_map:
                        print(f"   ⚠ Warning: Channel not found: {channel_name}")
                        continue
                    
                    channel_id = channel_map[channel_name]
                    
                    links_data.append({
                        'subcategory_id': subcat_id,
                        'channel_id': channel_id
                    })
        
        if not links_data:
            print("   ℹ No relationships to create")
            return True
        
        # Step 4: Upsert relationships
        # Note: Assuming unique constraint on (subcategory_id, channel_id)
        response = supabase.table('subcategory_channels').upsert(
            links_data,
            on_conflict='subcategory_id,channel_id'
        ).execute()
        
        print(f"   ✓ Successfully created {len(links_data)} subcategory-channel relationships")
        return True
        
    except Exception as e:
        print(f"   ✗ ERROR seeding relationships: {e}")
        return False


def main():
    """
    Main execution function: orchestrates the seeding process.
    """
    print("\n" + "=" * 80)
    print("Starting database seeding process...")
    print("=" * 80)
    
    # Step 1: Seed channels
    if not seed_channels():
        print("\n❌ Failed to seed channels. Aborting.")
        sys.exit(1)
    
    # Step 2: Seed subcategories
    if not seed_subcategories():
        print("\n❌ Failed to seed subcategories. Aborting.")
        sys.exit(1)
    
    # Step 3: Seed relationships
    if not seed_links():
        print("\n❌ Failed to seed relationships. Aborting.")
        sys.exit(1)
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ Database seeding completed successfully!")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Verify data in Supabase dashboard")
    print("  2. Run ingest.py to fetch videos from YouTube API")
    print("  3. Deploy your application")
    print("=" * 80)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Seeding interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n✗ FATAL ERROR: {e}")
        sys.exit(1)

