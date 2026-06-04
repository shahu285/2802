import logging
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from email.utils import parsedate_to_datetime
from langchain_google_genai import ChatGoogleGenerativeAI

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

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY is missing from the .env file")
    raise ValueError("GEMINI_API_KEY is missing from the .env file")

logger.info("GEMINI_API_KEY loaded successfully")

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
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.65,
            google_api_key=GEMINI_API_KEY
        )

        response = llm.invoke(system_prompt.format(headline=headline))
        post_text = response.content.strip()
        
        logger.info(f"Generated post for: {headline[:50]}...")
        return post_text

    except Exception as e:
        logger.error(f"Error generating post for headline: {headline} - Error: {e}")
        return ""
# =====================================================================
# 🚀 MAIN EXECUTION
# =====================================================================
if __name__ == "__main__":
    from reporter import fetch_major_headlines

    logger.info("Fetching recent headlines...")
    all_headlines = fetch_major_headlines()
    
    # Filter to only include news from last 24 hours
    recent_headlines = get_recent_headlines(all_headlines, hours=24)
    
    print(f"\n--- 📰 Recent Headlines (Last 24 Hours) ---")
    for i, article in enumerate(recent_headlines[:5], 1):
        print(f"{i}. [{article['source']}] {article['headline']}")
    print("------------------------------------------\n")
    
    # Generate posts for recent headlines
    if recent_headlines:
        logger.info("Generating journalistic posts for recent headlines...")
        for article in recent_headlines[:3]:
            post = generate_journalistic_post(article["headline"])
            print(f"Headline: {article['headline'][:60]}...")
            print(f"Post: {post}")
            print(f"Chars: {len(post)}\n")