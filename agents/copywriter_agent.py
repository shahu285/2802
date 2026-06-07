import logging
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from email.utils import parsedate_to_datetime
from langchain_groq import ChatGroq

# =====================================================================
# 🪵 SYSTEM LOGGING CONFIGURATION
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (Node: %(name)s) -> %(message)s",
    handlers=[
        logging.FileHandler("newsroom.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Sports_Journalist")

# =====================================================================
# 🔐 ENVIRONMENT VARIABLES
# =====================================================================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    logger.error("GROQ_API_KEY is missing from the .env file")
    raise ValueError("GROQ_API_KEY is missing from the .env file")

logger.info("GROQ_API_KEY loaded successfully")

# =====================================================================
# 🕐 RECENT HEADLINES FILTER
# =====================================================================
def get_recent_headlines(headlines: list, hours: int = 24) -> list:
    """
    Filters articles to only include those published within the last N hours.
    """
    cutoff_time = datetime.now().replace(tzinfo=None) - timedelta(hours=hours)
    recent = []
    
    for article in headlines:
        pub_date = article.get("pub_date")
        if pub_date:
            try:
                if pub_date.replace(tzinfo=None) > cutoff_time:
                    recent.append(article)
            except Exception:
                pass
    
    logger.info(f"Filtered {len(headlines)} articles down to {len(recent)} from last {hours} hours")
    return recent

# =====================================================================
# 📝 JOURNALISTIC POST GENERATOR
# =====================================================================
def generate_journalistic_post(headline: str) -> str:
    """
    Transforms raw headlines into viral micro-blog posts.
    """
    system_prompt = """You are an advanced AI Sports Journalist capable of analyzing news severity and adjusting post layouts dynamically to maintain editorial credibility.

STEP 1: ANALYZE SEVERITY TIER
Read the headline and classify it into one of these three distinct tiers:

TIER 1 (High Alert): Major retirements, captaincy handovers, tournament final results, critical injury news of star players.

TIER 2 (Regular News): Match updates, team press conferences, squad travel arrivals, general training camp notes.

TIER 3 (Features/Stats): Milestone anniversaries, player quotes, statistical records, legend opinions.

STEP 2: APPLY CONDITIONAL FORMATTING

IF TIER 1: Start the first line with exactly: '🚨BREAKING' or '🚨UPDATE' followed by a clean line break. Keep it high-velocity, dramatic, and punchy. Conclude with a single-emoji closer (e.g., 🔥, ⏳).

IF TIER 2: DO NOT include any alert flags or breaking text. Start directly with a clean, professional, matter-of-fact sentence. Use clean line breaks for readability. Use a maximum of 1 standard emoji at the end (e.g., 🏏, ⚽).

IF TIER 3: Write in a engaging, storytelling, or reflective tone. No breaking text. You may use a calm emoji hook (e.g., 📸, 👑, 📊).

CRITICAL: Output ONLY the final generated post text. Do not output your tier classification explanation, bracketed indicators, or markdown tags.

STRICT CHARACTER LIMIT: Your entire output must be under 280 characters. This is non-negotiable. Count your words carefully.

Headline to transform: '{headline}'
Drafted Post:"""

    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.65,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

        response = llm.invoke(system_prompt.format(headline=headline))
        post_text = response.content.strip()
        
        logger.info(f"Generated post for: {headline[:50]}...")
        return post_text

    except Exception as e:
        logger.error(f"Error generating post for headline: {headline} - Error: {e}")
        return ""
# =====================================================================
# 🚀 MAIN EXECUTION - MULTI-AGENT PIPELINE TEST
# =====================================================================
if __name__ == "__main__":
    from beat_reporter import fetch_major_headlines
    from regional_editor import evaluate_headline_significance
    from datetime import datetime, timedelta

    logger.info("=== Starting Multi-Agent Pipeline Test ===")
    
    # Step 1: Fetch raw headlines
    logger.info("Fetching raw headlines from all RSS feeds...")
    all_headlines = fetch_major_headlines()
    
    # Filter to last 24 hours
    cutoff_time = datetime.now().replace(tzinfo=None) - timedelta(hours=24)
    recent_headlines = [
        h for h in all_headlines 
        if h.get("pub_date") and h["pub_date"].replace(tzinfo=None) > cutoff_time
    ]
    
    logger.info(f"Total headlines: {len(all_headlines)} | Last 24h: {len(recent_headlines)}")
    
    # Step 2: Find first headline that passes regional editor filter
    approved_headline = None
    for article in recent_headlines:
        headline = article["headline"]
        is_approved = evaluate_headline_significance(headline)
        
        if is_approved:
            approved_headline = article
            logger.info(f"First approved headline found: {headline[:50]}...")
            break
    
    # Step 3: Generate journalistic post from approved headline
    if approved_headline:
        raw_headline = approved_headline["headline"]
        logger.info("Passing to Sports_Journalist for post generation...")
        
        final_post = generate_journalistic_post(raw_headline)
        
        # Output clean comparison
        print("\n" + "="*60)
        print("📰 RAW HEADLINE (from Beat_Reporter)")
        print("="*60)
        print(f"{raw_headline}")
        print(f"Source: {approved_headline['source']}")
        
        print("\n" + "="*60)
        print("✨ FINAL JOURNALISTIC POST (from Sports_Journalist)")
        print("="*60)
        print(final_post)
        print(f"\nCharacter count: {len(final_post)}/280")
        print("="*60 + "\n")
    else:
        logger.warning("No headlines passed the regional editor filter.")