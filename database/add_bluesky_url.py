"""
Helper script to add bluesky_url column to pending_posts table
Run this once to add the new column
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

print("🔧 Adding bluesky_url column to pending_posts table...")
print("\n⚠️  Please run this SQL in Supabase SQL Editor:")
print("\n" + "="*60)
print("""
ALTER TABLE pending_posts 
ADD COLUMN IF NOT EXISTS bluesky_url TEXT;

COMMENT ON COLUMN pending_posts.bluesky_url 
IS 'URL of the published post on Bluesky';
""")
print("="*60)
print("\nSteps:")
print("1. Go to: https://supabase.com/dashboard/project/lmwohypczyicnznoqejo")
print("2. Click 'SQL Editor' in the left sidebar")
print("3. Click 'New Query'")
print("4. Paste the SQL above")
print("5. Click 'Run' (or press Ctrl+Enter)")
print("\n✅ Once done, the column will be available!")
