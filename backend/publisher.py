"""
Bluesky Publisher for Newsroom AI
Layer 3: Handles posting to Bluesky social network
"""
import logging
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# =====================================================================
# 🪵 LOGGING CONFIGURATION
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (Node: %(name)s) -> %(message)s",
    handlers=[
        logging.FileHandler("../newsroom.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Publisher")

# =====================================================================
# 🔐 ENVIRONMENT VARIABLES
# =====================================================================
load_dotenv()

BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")

if not BLUESKY_HANDLE or not BLUESKY_PASSWORD:
    logger.error("BLUESKY_HANDLE or BLUESKY_PASSWORD missing from .env")
    raise ValueError("Bluesky credentials missing")

# Bluesky API endpoints
BskyAPI = "https://bsky.social/xrpc"

# =====================================================================
# 🔐 AUTHENTICATION
# =====================================================================
def get_session() -> dict:
    """
    Authenticate with Bluesky and get session token
    """
    try:
        response = requests.post(
            f"{BskyAPI}/com.atproto.server.createSession",
            json={
                "identifier": BLUESKY_HANDLE,
                "password": BLUESKY_PASSWORD
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Authenticated as {data.get('did')}")
            return {
                "access_jwt": data.get("accessJwt"),
                "did": data.get("did")
            }
        else:
            logger.error(f"Authentication failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error authenticating: {e}")
        return None

# =====================================================================
# 📤 POST PUBLISHING
# =====================================================================
def publish_post(text: str, image_url: str = None) -> dict:
    """
    Publish a post to Bluesky
    
    Args:
        text: The post content (max 300 chars for Bluesky)
        image_url: Optional image URL to attach
        
    Returns:
        dict with success status and post details
    """
    session = get_session()
    
    if not session:
        return {
            "success": False,
            "error": "Failed to authenticate with Bluesky"
        }
    
    access_jwt = session["access_jwt"]
    did = session["did"]
    
    try:
        # Prepare the post record
        from datetime import datetime, timezone
        record = {
            "$type": "app.bsky.feed.post",
            "text": text[:300],  # Bluesky limit is 300 chars
            "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }
        
        headers = {
            "Authorization": f"Bearer {access_jwt}",
            "Content-Type": "application/json"
        }
        
        # Create the post
        response = requests.post(
            f"{BskyAPI}/com.atproto.repo.createRecord",
            json={
                "repo": did,
                "collection": "app.bsky.feed.post",
                "record": record
            },
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            uri = data.get("uri", "")
            logger.info(f"✅ Post published: {uri}")
            
            # If there's an image, we'd need to upload it first
            # and then create a post with the image embedded
            # This is more complex - for now, just post text
            
            return {
                "success": True,
                "uri": uri,
                "cid": data.get("cid")
            }
        else:
            logger.error(f"Failed to publish: {response.status_code} - {response.text}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
            
    except Exception as e:
        logger.error(f"Error publishing post: {e}")
        return {
            "success": False,
            "error": str(e)
        }

# =====================================================================
# 🖼️ IMAGE UPLOAD + POST (Advanced)
# =====================================================================
def publish_post_with_image(text: str, image_url: str) -> dict:
    """
    Upload image to Bluesky and create post with image
    
    Note: This requires:
    1. Download the image
    2. Upload to Bluesky blob storage
    3. Create post with image embed
    """
    session = get_session()
    if not session:
        return {"success": False, "error": "Authentication failed"}
    
    access_jwt = session["access_jwt"]
    did = session["did"]
    
    headers = {
        "Authorization": f"Bearer {access_jwt}"
    }
    
    try:
        # Step 1: Download image
        logger.info(f"Downloading image from: {image_url}")
        img_response = requests.get(image_url, timeout=30)
        
        if img_response.status_code != 200:
            return {"success": False, "error": "Failed to download image"}
        
        # Determine content type
        content_type = img_response.headers.get("Content-Type", "image/jpeg")
        if "png" in content_type.lower():
            ext = "png"
        else:
            ext = "jpg"
        
        # Step 2: Upload blob
        blob_response = requests.post(
            f"{BskyAPI}/com.atproto.repo.uploadBlob",
            headers={
                "Authorization": f"Bearer {access_jwt}",
                "Content-Type": content_type
            },
            data=img_response.content
        )
        
        if blob_response.status_code != 200:
            logger.warning(f"Blob upload failed: {blob_response.status_code}")
            # Fall back to text-only post
            return publish_post(text)
        
        blob_data = blob_response.json()
        blob_ref = blob_data.get("blob")
        
        # Step 3: Create post with image embed
        from datetime import datetime, timezone
        record = {
            "$type": "app.bsky.feed.post",
            "text": text[:300],
            "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "embed": {
                "$type": "app.bsky.embed.images",
                "images": [{
                    "alt": "News image",
                    "image": blob_ref
                }]
            }
        }
        
        post_response = requests.post(
            f"{BskyAPI}/com.atproto.repo.createRecord",
            json={
                "repo": did,
                "collection": "app.bsky.feed.post",
                "record": record
            },
            headers=headers
        )
        
        if post_response.status_code == 200:
            data = post_response.json()
            logger.info(f"✅ Post with image published: {data.get('uri')}")
            return {
                "success": True,
                "uri": data.get("uri"),
                "cid": data.get("cid")
            }
        else:
            logger.error(f"Failed to create post: {post_response.text}")
            return {"success": False, "error": post_response.text}
            
    except Exception as e:
        logger.error(f"Error publishing post with image: {e}")
        return {"success": False, "error": str(e)}

# =====================================================================
# 🚀 MAIN EXECUTION - TEST
# =====================================================================
if __name__ == "__main__":
    logger.info("Testing Bluesky publisher...")
    
    # Test authentication
    session = get_session()
    if session:
        print(f"✅ Authenticated as: {session['did']}")
        
        # Test text-only post
        test_text = "🧪 Test post from Newsroom AI! 🏏"
        result = publish_post(test_text)
        print(f"Text post result: {result}")
    else:
        print("❌ Authentication failed")