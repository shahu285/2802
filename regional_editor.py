import logging
import os
from dotenv import load_dotenv
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

logger = logging.getLogger("Regional_Editor")

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
# 🧠 HEADLINE SIGNIFICANCE EVALUATOR
# =====================================================================
def evaluate_headline_significance(headline: str) -> bool:
    """
    Evaluates if a headline is significant for Indian sports coverage.
    """
    system_prompt = """You are an Indian Sports Media Analyst filtering news based on regional audience consumption metrics:

CRICKET: ~65% market share (IPL, Internationals, top-tier domestic players). [ALLOW]

KABADDI: 200M+ league watch metrics (Pro Kabaddi League). [ALLOW]

FOOTBALL: High demographic engagement (UEFA Champions League, Premier League, ISL). [ALLOW]

MULTI-SPORT INTEL: Key international milestones in Badminton, Chess, and Hockey featuring core Indian representation. [ALLOW]

US REGIONAL SPORTS: <0.5% market footprint in India (NFL, MLB, NBA, Baseball, Ice Hockey). [BLOCK]

MINOR EVENTS: Local gossip, routine practice ground announcements, or generic fit-check updates. [BLOCK]

Review the headline. Output exactly one word: ALLOW or BLOCK."""

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.1,
            google_api_key=GEMINI_API_KEY
        )

        response = llm.invoke(f"{system_prompt}\n\nHeadline: {headline}")
        response_text = response.content.strip().upper()

        if "ALLOW" in response_text:
            logger.info(f"APPROVED: {headline}")
            return True
        else:
            logger.info(f"REJECTED: {headline}")
            return False

    except Exception as e:
        logger.warning(f"API timeout or error for headline: {headline} - Error: {e}")
        return False


# =====================================================================
# 🚀 MAIN EXECUTION
# =====================================================================
if __name__ == "__main__":
    from beat_reporter import fetch_major_headlines

    logger.info("Fetching live headlines for evaluation...")
    headlines = fetch_major_headlines()

    print("\n--- 🧪 HEADLINE EVALUATION RESULTS ---")
    for i, article in enumerate(headlines[:5], 1):
        headline = article["headline"]
        result = evaluate_headline_significance(headline)
        status = "✅ ALLOWED" if result else "❌ REJECTED"
        print(f"{i}. {status}")
        print(f"   Headline: {headline}")
        print(f"   Source: {article['source']}\n")
    print("--------------------------------------\n")