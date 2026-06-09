import logging
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (Node: %(name)s) -> %(message)s",
    handlers=[
        logging.FileHandler("newsroom.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Pipeline_Test")

load_dotenv()

# =====================================================================
# IMPORT ALL AGENTS
# =====================================================================
from agents.beat_reporter import fetch_major_headlines
from agents.regional_editor import evaluate_headline_significance
from agents.copywriter_agent import generate_journalistic_post
from agents.photojournalist import generate_image as generate_image_prompt, fetch_image_from_prompt
from database.database_manager import insert_pending_post

# =====================================================================
# PIPELINE EXECUTION
# =====================================================================
if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🚀 STARTING FULL MULTI-AGENT PIPELINE TEST")
    logger.info("=" * 60)
    
    # STEP 1: Beat_Reporter - Fetch headlines
    logger.info("\n📡 STEP 1: Beat_Reporter fetching headlines...")
    all_headlines = fetch_major_headlines()
    
    # Filter to last 24 hours
    cutoff_time = datetime.now().replace(tzinfo=None) - timedelta(hours=24)
    recent_headlines = [
        h for h in all_headlines 
        if h.get("pub_date") and h["pub_date"].replace(tzinfo=None) > cutoff_time
    ]
    logger.info(f"Total: {len(all_headlines)} | Last 24h: {len(recent_headlines)}")
    
    # STEP 2: Regional_Editor - Evaluate and approve multiple headlines
    logger.info("\n🔍 STEP 2: Regional_Editor evaluating headlines...")
    
    approved_headlines = []
    for article in recent_headlines:
        headline = article["headline"]
        if evaluate_headline_significance(headline):
            approved_headlines.append(article)
            if len(approved_headlines) >= 5:  # Process up to 5 posts
                break
    
    if not approved_headlines:
        logger.error("No headlines passed the regional editor filter!")
        exit(1)
    
    logger.info(f"✅ Approved {len(approved_headlines)} headlines for processing")
    
    # Process each approved headline
    for idx, approved_headline in enumerate(approved_headlines, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"📰 PROCESSING POST {idx}/{len(approved_headlines)}")
        logger.info(f"{'='*60}")
        
        raw_headline = approved_headline["headline"]
        source = approved_headline["source"]
        logger.info(f"Headline: {raw_headline[:60]}...")
        
        # STEP 3: Copywriter_Agent - Generate viral post
        logger.info(f"\n✍️ STEP 3.{idx}: Copywriter_Agent generating post...")
        viral_post = generate_journalistic_post(raw_headline)
        logger.info("✅ Viral post generated")
        
        # STEP 4: Photojournalist - Get image
        logger.info(f"\n🎨 STEP 4.{idx}: Photojournalist getting image...")
        image_url = fetch_image_from_prompt(raw_headline, raw_headline)
        logger.info("✅ Image retrieved")
        
        # STEP 5: Save to Database (Supabase)
        logger.info(f"\n💾 STEP 5.{idx}: Saving to Supabase database...")
        # Determine severity tier from the post content
        if viral_post.startswith("🚨BREAKING") or viral_post.startswith("🚨UPDATE"):
            severity_tier = "Tier 1"
        elif any(emoji in viral_post for emoji in ["🏏", "⚽", "🏅", "🎯"]):
            severity_tier = "Tier 2"
        else:
            severity_tier = "Tier 3"
        
        saved_post = insert_pending_post(
            raw_headline=raw_headline,
            styled_text=viral_post,
            image_url=image_url,
            severity_tier=severity_tier,
            source_feed=source
        )
        
        if saved_post:
            logger.info(f"✅ Post {idx} saved to database with ID: {saved_post['id']}")
        else:
            logger.error(f"❌ Failed to save post {idx} to database")
        
        # Print summary for this post
        print("\n" + "=" * 70)
        print(f"📰 POST {idx}: {source}")
        print("=" * 70)
        print(f"Raw: {raw_headline[:80]}...")
        print(f"Styled: {viral_post[:100]}...")
        print(f"Tier: {severity_tier}")
        print("=" * 70)
    
    # =====================================================================
    # FINAL SUMMARY
    # =====================================================================
    print("\n" + "=" * 70)
    print(f"✅ PIPELINE COMPLETE - {len(approved_headlines)} POSTS PROCESSED")
    print("=" * 70)
    print(f"📊 Total headlines fetched: {len(all_headlines)}")
    print(f"📊 Recent (24h): {len(recent_headlines)}")
    print(f"📊 Approved: {len(approved_headlines)}")
    print(f"📊 Saved to database: {len(approved_headlines)}")
    print("=" * 70 + "\n")