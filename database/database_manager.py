import logging
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# =====================================================================
# 🪵 SYSTEM LOGGING CONFIGURATION
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (Node: %(name)s) -> %(message)s",
    handlers=[
        logging.FileHandler("../newsroom.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Database_Manager")

# =====================================================================
# 🔐 ENVIRONMENT VARIABLES
# =====================================================================
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    logger.error("SUPABASE_URL or SUPABASE_ANON_KEY missing from .env")
    raise ValueError("Supabase credentials missing")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
logger.info("Supabase client initialized successfully")

# =====================================================================
# 📥 INSERT POST TO DATABASE
# =====================================================================
def insert_pending_post(
    raw_headline: str,
    styled_text: str,
    image_url: str = None,
    severity_tier: str = "Tier 2",
    source_feed: str = None
) -> dict:
    """
    Inserts a new post into the pending_posts table.
    
    Returns the inserted record with its ID.
    """
    try:
        data = {
            "raw_headline": raw_headline,
            "styled_text": styled_text,
            "image_url": image_url,
            "severity_tier": severity_tier,
            "source_feed": source_feed,
            "status": "pending"
        }
        
        response = supabase.table("pending_posts").insert(data).execute()
        
        if response.data:
            post_id = response.data[0]["id"]
            logger.info(f"✅ Post inserted to database: {post_id}")
            return response.data[0]
        else:
            logger.error("Failed to insert post - no data returned")
            return None
            
    except Exception as e:
        logger.error(f"Error inserting post to Supabase: {e}")
        return None

# =====================================================================
# 📋 FETCH PENDING POSTS
# =====================================================================
def get_pending_posts() -> list:
    """
    Fetches all posts with status 'pending'.
    """
    try:
        response = supabase.table("pending_posts").select("*").eq("status", "pending").execute()
        logger.info(f"Fetched {len(response.data)} pending posts")
        return response.data
    except Exception as e:
        logger.error(f"Error fetching pending posts: {e}")
        return []

# =====================================================================
# 📋 FETCH ALL POSTS
# =====================================================================
def get_all_posts() -> list:
    """
    Fetches all posts from the database.
    """
    try:
        response = supabase.table("pending_posts").select("*").order("created_at", desc=True).execute()
        logger.info(f"Fetched {len(response.data)} total posts")
        return response.data
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        return []

# =====================================================================
# 📋 FETCH POST BY ID
# =====================================================================
def get_post_by_id(post_id: str) -> dict:
    """
    Fetches a single post by its ID.
    """
    try:
        response = supabase.table("pending_posts").select("*").eq("id", post_id).execute()
        if response.data and len(response.data) > 0:
            logger.info(f"Fetched post {post_id}")
            return response.data[0]
        else:
            logger.warning(f"Post {post_id} not found")
            return None
    except Exception as e:
        logger.error(f"Error fetching post by ID: {e}")
        return None

# =====================================================================
# ✅ UPDATE POST STATUS
# =====================================================================
def update_post_status(post_id: str, new_status: str, bluesky_url: str = None) -> bool:
    """
    Updates the status of a post (approved/rejected) and optionally stores Bluesky URL.
    
    Args:
        post_id: The UUID of the post
        new_status: Either 'approved' or 'rejected'
        bluesky_url: Optional URL of the published Bluesky post
    """
    if new_status not in ["approved", "rejected"]:
        logger.error(f"Invalid status: {new_status}")
        return False
    
    try:
        update_data = {"status": new_status}
        if bluesky_url:
            update_data["bluesky_url"] = bluesky_url
            
        response = supabase.table("pending_posts").update(update_data).eq("id", post_id).execute()
        
        if response.data:
            logger.info(f"✅ Post {post_id} status updated to {new_status}")
            if bluesky_url:
                logger.info(f"✅ Bluesky URL saved: {bluesky_url}")
            return True
        else:
            logger.error(f"Failed to update post {post_id}")
            return False
            
    except Exception as e:
        logger.error(f"Error updating post status: {e}")
        return False

# =====================================================================
# 🗑️ DELETE POST
# =====================================================================
def delete_post(post_id: str) -> bool:
    """
    Deletes a post from the database.
    """
    try:
        response = supabase.table("pending_posts").delete().eq("id", post_id).execute()
        logger.info(f"✅ Post {post_id} deleted")
        return True
    except Exception as e:
        logger.error(f"Error deleting post: {e}")
        return False

# =====================================================================
# 🚀 MAIN EXECUTION - TEST
# =====================================================================
if __name__ == "__main__":
    logger.info("Testing database connection...")
    
    # Test fetch
    posts = get_all_posts()
    print(f"\nTotal posts in database: {len(posts)}")
    
    # Test insert
    test_post = insert_pending_post(
        raw_headline="Test: Dhoni announces retirement",
        styled_text="🚨BREAKING: MS Dhoni announces retirement from IPL after 15 seasons. The legend departs as the most successful captain in IPL history. 🔥",
        image_url="https://example.com/test.jpg",
        severity_tier="Tier 1",
        source_feed="Cricket Feed"
    )
    
    if test_post:
        print(f"✅ Test post inserted with ID: {test_post['id']}")
        
        # Test update
        update_post_status(test_post['id'], "approved")
        print(f"✅ Status updated to approved")
        
        # Test delete
        delete_post(test_post['id'])
        print(f"✅ Test post deleted")
    
    print("\nDatabase manager test complete!")