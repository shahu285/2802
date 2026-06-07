"""
FastAPI Backend for Newsroom AI
Layer 3: API Gateway for post management
"""
import os
import logging
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import database functions
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.database_manager import (
    get_pending_posts,
    get_all_posts,
    update_post_status,
    delete_post,
    insert_pending_post
)

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

logger = logging.getLogger("FastAPI_Backend")

# =====================================================================
# 🔐 ENVIRONMENT VARIABLES
# =====================================================================
load_dotenv()

# =====================================================================
# 🚀 FASTAPI APP SETUP
# =====================================================================
app = FastAPI(
    title="Newsroom AI API",
    description="Backend API for managing news posts",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================================
# 📦 PYDANTIC MODELS
# =====================================================================
class Post(BaseModel):
    id: str
    raw_headline: str
    styled_text: str
    image_url: Optional[str] = None
    severity_tier: str
    status: str
    source_feed: Optional[str] = None
    created_at: str

class PostCreate(BaseModel):
    raw_headline: str
    styled_text: str
    image_url: Optional[str] = None
    severity_tier: str = "Tier 2"
    source_feed: Optional[str] = None

# =====================================================================
# 📡 API ENDPOINTS
# =====================================================================

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Newsroom AI API is running",
        "version": "1.0.0",
        "endpoints": {
            "pending": "/api/posts/pending",
            "all": "/api/posts/all",
            "approve": "/api/posts/{id}/approve",
            "reject": "/api/posts/{id}/reject",
            "delete": "/api/posts/{id}"
        }
    }

@app.get("/api/posts/pending", response_model=List[Post])
def get_pending():
    """
    Fetch all posts with status='pending'
    """
    try:
        posts = get_pending_posts()
        # Convert datetime to string if it's not already
        for post in posts:
            if post.get("created_at") and not isinstance(post["created_at"], str):
                post["created_at"] = post["created_at"].isoformat()
        logger.info(f"Fetched {len(posts)} pending posts")
        return posts
    except Exception as e:
        logger.error(f"Error fetching pending posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/posts/all", response_model=List[Post])
def get_all():
    """
    Fetch all posts (pending + history)
    """
    try:
        posts = get_all_posts()
        # Convert datetime to string if it's not already
        for post in posts:
            if post.get("created_at") and not isinstance(post["created_at"], str):
                post["created_at"] = post["created_at"].isoformat()
        logger.info(f"Fetched {len(posts)} total posts")
        return posts
    except Exception as e:
        logger.error(f"Error fetching all posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/posts/{post_id}/approve")
def approve_post(post_id: str):
    """
    Approve a post - changes status to 'approved' and triggers publishing
    """
    try:
        # Update status to approved
        success = update_post_status(post_id, "approved")
        
        if not success:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # TODO: Trigger publisher.py to post to Bluesky
        logger.info(f"Post {post_id} approved - ready for publishing")
        
        return {
            "success": True,
            "message": f"Post {post_id} approved and queued for publishing"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error approving post: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/posts/{post_id}/reject")
def reject_post(post_id: str):
    """
    Reject a post - changes status to 'rejected'
    """
    try:
        success = update_post_status(post_id, "rejected")
        
        if not success:
            raise HTTPException(status_code=404, detail="Post not found")
        
        logger.info(f"Post {post_id} rejected")
        
        return {
            "success": True,
            "message": f"Post {post_id} rejected"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rejecting post: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/posts/{post_id}")
def delete_post_endpoint(post_id: str):
    """
    Delete a post from the database
    """
    try:
        success = delete_post(post_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Post not found")
        
        logger.info(f"Post {post_id} deleted")
        
        return {
            "success": True,
            "message": f"Post {post_id} deleted"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting post: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/posts", response_model=Post)
def create_post(post: PostCreate):
    """
    Create a new post (manual entry)
    """
    try:
        result = insert_pending_post(
            raw_headline=post.raw_headline,
            styled_text=post.styled_text,
            image_url=post.image_url,
            severity_tier=post.severity_tier,
            source_feed=post.source_feed
        )
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create post")
        
        if result.get("created_at"):
            result["created_at"] = result["created_at"].isoformat()
            
        logger.info(f"Created new post: {result['id']}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =====================================================================
# 🚀 MAIN EXECUTION
# =====================================================================
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server on http://127.0.0.1:8000")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )