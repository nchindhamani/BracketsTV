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

#!/usr/bin/env python3
"""
BracketsTV Database Seeding Script
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from config_data import MASTER_CHANNEL_LIST, APP_CONFIG

try:
    from supabase import create_client, Client
except ImportError:
    print("ERROR: supabase-py not installed.")
    print("Install with: pip install supabase")
    sys.exit(1)

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting BracketsTV Database Seeding")
print(f"Supabase URL: {SUPABASE_URL}")
print("=" * 80)


def seed_channels():
    print("\n📺 Seeding channels table...")
    try:
        channels_to_seed = []
        for channel_name, channel_info in MASTER_CHANNEL_LIST.items():
            channels_to_seed.append({
                # FIX: Use 'channel_name' and 'channel_handle' to match DB schema
                'channel_name': channel_name,
                'channel_id': channel_info['channel_id'],
                'channel_handle': channel_info['channel_handle'],
                'is_active': True
            })

        if channels_to_seed:
            supabase.table('channels').upsert(
                channels_to_seed,
                on_conflict='channel_id'
            ).execute()
        
        print(f"   ✓ Successfully seeded {len(channels_to_seed)} channels")
        return True
    except Exception as e:
        print(f"   ✗ ERROR seeding channels: {e}")
        return False


def seed_subcategories():
    print("\n📁 Seeding subcategories table...")
    try:
        subcategories_to_seed = []
        for category_config in APP_CONFIG:
            main_category = category_config['main_category']
            for subcat in category_config['subcategories']:
                # FIX: Use 'main_category' to match DB schema
                subcategories_to_seed.append({
                    'main_category': main_category,
                    'name': subcat['name'],
                    'strategy': subcat['strategy'],
                    'search_query': subcat.get('search_query', ''),
                    'is_active': subcat.get('is_active', True)
                })
        
        if subcategories_to_seed:
            # FIX: Use 'main_category,name' for on_conflict
            supabase.table('subcategories').upsert(
                subcategories_to_seed,
                on_conflict='main_category,name'
            ).execute()

        print(f"   ✓ Successfully seeded {len(subcategories_to_seed)} subcategories")
        return True
    except Exception as e:
        print(f"   ✗ ERROR seeding subcategories: {e}")
        return False


def seed_links():
    print("\n🔗 Seeding subcategory_channels relationships...")
    try:
        print("   → Clearing existing relationships...")
        supabase.table('subcategory_channels').delete().neq('subcategory_id', '00000000-0000-0000-0000-000000000000').execute()
        print("   ✓ Cleared existing relationships")

        # Fetch all channels and subcategories into memory maps for efficiency
        channels_res = supabase.table('channels').select('id, channel_name').execute()
        channel_map = {c['channel_name']: c['id'] for c in channels_res.data}

        subcats_res = supabase.table('subcategories').select('id, main_category, name').execute()
        subcat_map = {(sc['main_category'], sc['name']): sc['id'] for sc in subcats_res.data}
        
        links_to_seed = []
        for category_config in APP_CONFIG:
            main_category = category_config['main_category']
            for subcat in category_config['subcategories']:
                channel_names = subcat.get('channels', [])
                if not channel_names:
                    continue
                
                subcat_key = (main_category, subcat['name'])
                if subcat_key in subcat_map:
                    subcat_id = subcat_map[subcat_key]
                    for channel_name in channel_names:
                        if channel_name in channel_map:
                            channel_id = channel_map[channel_name]
                            links_to_seed.append({
                                'subcategory_id': subcat_id,
                                'channel_id': channel_id
                            })
                        else:
                            print(f"   ⚠ Warning: Channel '{channel_name}' not found in database map.")
                else:
                    print(f"   ⚠ Warning: Subcategory '{subcat['name']}' not found in database map.")

        if links_to_seed:
            supabase.table('subcategory_channels').insert(links_to_seed).execute()

        print(f"   ✓ Successfully created {len(links_to_seed)} subcategory-channel relationships")
        return True
    except Exception as e:
        print(f"   ✗ ERROR seeding relationships: {e}")
        return False


def main():
    print("\n" + "=" * 80)
    print("Starting database seeding process...")
    print("=" * 80)
    
    if not seed_channels():
        print("\n❌ Failed to seed channels. Aborting.")
        sys.exit(1)
    
    if not seed_subcategories():
        print("\n❌ Failed to seed subcategories. Aborting.")
        sys.exit(1)

    if not seed_links():
        print("\n❌ Failed to seed relationships. Aborting.")
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print("✅ Database seeding completed successfully!")
    print("=" * 80)


if __name__ == '__main__':
    main()