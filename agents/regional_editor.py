import logging
import os
from dotenv import load_dotenv
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

logger = logging.getLogger("Regional_Editor")

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
# 🧠 HEADLINE SIGNIFICANCE EVALUATOR
# =====================================================================
def evaluate_headline_significance(headline: str) -> bool:
    """
    Evaluates if a headline is significant for Indian sports coverage.
    """
    system_prompt = """You are an Indian Sports Media Analyst filtering news based on regional audience consumption metrics.

ALLOW the following:
✅ CRICKET: All cricket news (IPL, International, Domestic, Indian players, World Cup, T20, ODI, Test)
✅ KABADDI: Pro Kabaddi League, Indian kabaddi teams, kabaddi tournaments
✅ FOOTBALL: Premier League, Champions League, ISL (Indian Super League), La Liga, international football, FIFA
✅ BADMINTON: All badminton news (Indian players like PV Sindhu, Saina Nehwal, tournaments, Olympics)
✅ HOCKEY: Field hockey (Indian men's/women's teams, FIH tournaments, Olympics, World Cup)
✅ WRESTLING: Indian wrestlers (Bajrang Punia, Vinesh Phogat, Olympics, World Championships)
✅ TENNIS: Indian players (Leander Paes, Sania Mirza), Grand Slams, ATP/WTA
✅ ATHLETICS: Track and field, marathons, Indian athletes, Olympics
✅ CHESS: Indian players (Viswanathan Anand, Gukesh, Praggnanandhaa), tournaments
✅ BOXING: Indian boxers (Mary Kom, Vijender Singh), Olympics, World Championships
✅ SHOOTING: Indian shooters, Olympics, World Championships
✅ OLYMPIC SPORTS: Any Olympic sport featuring Indian athletes or major international events
✅ FORMULA 1: F1 news (popular in India)
✅ MIXED MARTIAL ARTS: UFC, ONE Championship, Indian fighters

BLOCK the following:
❌ US-ONLY SPORTS: NFL, NBA, MLB, NHL, Baseball, Ice Hockey, American Football (unless Indian connection)
❌ MINOR GOSSIP: Celebrity personal life, fashion, unverified rumors
❌ ROUTINE UPDATES: Practice sessions, minor team announcements without news value

Review the headline and decide if Indian sports fans would be interested.
Output exactly ONE word: ALLOW or BLOCK."""

    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            groq_api_key=os.getenv("GROQ_API_KEY")
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