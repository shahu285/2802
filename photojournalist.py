import logging
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from duckduckgo_search import DDGS

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

logger = logging.getLogger("Photojournalist")

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
# 🎨 IMAGE PROMPT GENERATOR
# =====================================================================
def generate_image_prompt(headline: str) -> str:
    """
    Generates a detailed image generation prompt based on a sports headline.
    """
    system_prompt = """You are a Sports Photojournalist visual prompt engineer. Your task is to create vivid, descriptive image generation prompts for AI image generators.

GUIDELINES:
- Focus on the key visual elements from the headline (players, actions, venues, emotions)
- Include rich descriptive details: lighting, camera angle, colors, atmosphere
- Specify sports context: cricket field, football stadium, badminton court, etc.
- Capture the mood: celebration, tension, victory, defeat, anticipation
- Include Indian sports context where relevant (Indian team jerseys, stadiums, crowds)
- Keep the prompt under 200 words for optimal AI image generation
- Output ONLY the prompt, no explanations or markdown

Headline: '{headline}'
Visual Prompt:"""

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.7,
            google_api_key=GEMINI_API_KEY
        )

        response = llm.invoke(system_prompt.format(headline=headline))
        prompt_text = response.content.strip()
        
        logger.info(f"Generated image prompt for: {headline[:50]}...")
        return prompt_text

    except Exception as e:
        logger.error(f"Error generating image prompt: {e}")
        return ""
# =====================================================================
# 🔍 IMAGE SEARCH FUNCTIONS
# =====================================================================
def get_image_query(headline: str) -> str:
    """
    Extracts a clean 3-to-4 word image search query from the headline.
    """
    system_prompt = """You are a photo editor. Extract the main person or team from this sports headline and output a clean, ultra-precise 3-to-4 word image search query. Optimize it to find professional action shots or portraits. Output ONLY the search query keywords with no punctuation, quote marks, or extra words."""

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.0,
            google_api_key=GEMINI_API_KEY
        )

        response = llm.invoke(f"{system_prompt}\n\nHeadline: {headline}")
        query = response.content.strip()
        
        logger.info(f"Extracted image query: {query}")
        return query

    except Exception as e:
        logger.error(f"Error extracting image query: {e}")
        return ""


def fetch_image_url(headline: str) -> str:
    """
    Searches for and returns a relevant image URL for the headline.
    """
    try:
        # Get the optimized search query
        query = get_image_query(headline)
        if not query:
            return ""
        
        # Search for images using DuckDuckGo
        ddgs = DDGS()
        results = ddgs.images(
            keywords=query,
            max_results=3
        )
        
        for result in results:
            url = result.get("url", "")
            if url and any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                logger.info(f"Found image URL: {url[:50]}...")
                return url
        
        logger.warning(f"No valid image found for query: {query}")
        return ""

    except Exception as e:
        logger.warning(f"Error fetching image URL (may be rate limited): {e}")
        return ""