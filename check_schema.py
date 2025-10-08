#!/usr/bin/env python3
"""
Quick script to check what columns actually exist in the videos table
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("=" * 80)
print("CHECKING ACTUAL DATABASE SCHEMA")
print("=" * 80)

# Try to get one row from videos table to see its structure
print("\n1. Checking 'videos' table:")
try:
    response = supabase.table('videos').select('*').limit(1).execute()
    if response.data and len(response.data) > 0:
        print(f"   ✓ Found {len(response.data)} row(s)")
        print(f"   Columns in 'videos' table: {list(response.data[0].keys())}")
    else:
        print("   ⚠ Table is empty, trying to insert a test row to see required columns...")
        # Try inserting a minimal test row
        test_video = {
            'video_id': 'TEST123',
            'title': 'Test Video'
        }
        try:
            supabase.table('videos').insert(test_video).execute()
            print("   ✓ Test insert succeeded with: video_id, title")
            # Clean up
            supabase.table('videos').delete().eq('video_id', 'TEST123').execute()
        except Exception as e:
            print(f"   Error: {e}")
except Exception as e:
    print(f"   ✗ Error querying videos table: {e}")

# Check subcategories table structure
print("\n2. Checking 'subcategories' table:")
try:
    response = supabase.table('subcategories').select('*').limit(1).execute()
    if response.data and len(response.data) > 0:
        print(f"   ✓ Found {len(response.data)} row(s)")
        print(f"   Columns: {list(response.data[0].keys())}")
        print(f"   Sample row: {response.data[0]}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Check channels table structure
print("\n3. Checking 'channels' table:")
try:
    response = supabase.table('channels').select('*').limit(1).execute()
    if response.data and len(response.data) > 0:
        print(f"   ✓ Found {len(response.data)} row(s)")
        print(f"   Columns: {list(response.data[0].keys())}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 80)

