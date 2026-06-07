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
    
    # STEP 2: Regional_Editor - Find first APPROVED FOOTBALL headline for variety
    logger.info("\n🔍 STEP 2: Regional_Editor evaluating headlines...")
    
    # First, try to find a football headline
    approved_headline = None
    for article in recent_headlines:
        headline = article["headline"]
        source = article.get("source", "")
        if "Football" in source or "football" in headline.lower():
            if evaluate_headline_significance(headline):
                approved_headline = article
                logger.info(f"✅ Found FOOTBALL headline: {headline[:60]}...")
                break
    
    # If no football, get any approved headline
    if not approved_headline:
        for article in recent_headlines:
            headline = article["headline"]
            if evaluate_headline_significance(headline):
                approved_headline = article
                break
    
    if not approved_headline:
        logger.error("No headlines passed the regional editor filter!")
        exit(1)
    
    raw_headline = approved_headline["headline"]
    source = approved_headline["source"]
    logger.info(f"✅ Approved headline: {raw_headline[:60]}...")
    
    # STEP 3: Copywriter_Agent - Generate viral post
    logger.info("\n✍️ STEP 3: Copywriter_Agent generating post...")
    viral_post = generate_journalistic_post(raw_headline)
    logger.info("✅ Viral post generated")
    
    # STEP 4: Photojournalist - Get image
    logger.info("\n🎨 STEP 4: Photojournalist getting image...")
    image_url = fetch_image_from_prompt(raw_headline, raw_headline)
    logger.info("✅ Image retrieved")
    
    # STEP 5: Save to Database (Supabase)
    logger.info("\n💾 STEP 5: Saving to Supabase database...")
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
        logger.info(f"✅ Post saved to database with ID: {saved_post['id']}")
    else:
        logger.error("❌ Failed to save post to database")
    
    # =====================================================================
    # FINAL OUTPUT
    # =====================================================================
    print("\n" + "=" * 70)
    print("📰 COMPLETE NEWS POST FROM MULTI-AGENT PIPELINE")
    print("=" * 70)
    
    print(f"\n📡 SOURCE: {source}")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "-" * 70)
    print("📰 RAW HEADLINE")
    print("-" * 70)
    print(raw_headline)
    
    print("\n" + "-" * 70)
    print("✨ VIRAL JOURNALISTIC POST")
    print("-" * 70)
    print(viral_post)
    print(f"\n📏 Character count: {len(viral_post)}/280")
    
    print("\n" + "-" * 70)
    print("🖼️ IMAGE")
    print("-" * 70)
    if image_url.startswith("data:image"):
        print("[Image generated as base64]")
        print(f"Data length: {len(image_url)} characters")
    else:
        print(image_url)
    
    print("\n" + "=" * 70)
    print("✅ PIPELINE COMPLETE")
    print("=" * 70 + "\n")