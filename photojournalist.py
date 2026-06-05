import logging
import os
import requests
import base64
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
# 🔐 TAVILY API KEY (for image search)
# =====================================================================
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if TAVILY_API_KEY:
    logger.info("TAVILY_API_KEY loaded successfully")
else:
    logger.warning("TAVILY_API_KEY not found in .env - image search will use fallback")
# =====================================================================
# 🔍 IMAGE SEARCH FUNCTIONS
# =====================================================================
def get_image_query(headline: str) -> str:
    """
    Extracts a clean 3-to-4 word image search query from the headline.
    """
    system_prompt = "You are a photo editor. Extract the main person or team from this sports headline and output a clean, ultra-precise 3-to-4 word image search query. Optimize it to find professional action shots or portraits. Output ONLY the search query keywords with no punctuation, quote marks, or extra words."

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


def generate_image(prompt: str) -> str:
    """
    Uses Tavily API to search for relevant images from Google Images.
    Filters out social media images (Instagram, Threads, Facebook).
    """
    FALLBACK_URL = "https://unsplash.com/photos/people-watching-game-of-cricket-during-sunset-mUtQXjjLPbw"
    
    # Domains to exclude (social media, not from Google Images)
    EXCLUDED_DOMAINS = [
        "facebook.com",
        "instagram.com", 
        "threads.net",
        "twitter.com",
        "x.com",
        "tiktok.com",
        "linkedin.com",
        "reddit.com",
        "pinterest.com",
        "snapchat.com",
        "whatsapp.com",
        "telegram.org"
    ]
    
    # Patterns to exclude (text-heavy images, thumbnails, quotes, press conference)
    EXCLUDED_PATTERNS = [
        "quote",
        "quotes",
        "infographic",
        "chart",
        "stat",
        "stats",
        "animation",
        "video",
        "player-profile",
        "headshot",
        "avatar",
        "icon",
        "logo",
        "banner",
        "illustration",
        "vector",
        "artwork",
        "cartoon",
        "meme",
        "text-on",
        "textoverlay",
        "wordart",
        "typo",
        # Press conference / media interaction
        "press",
        "pc ",
        "_pc",
        "conference",
        "interview",
        "media",
        "meeting",
        "address",
        "statement",
        # Motion/video frames
        "motion",
        "dm_",
        "videoframe",
        "frame",
        # Text overlay patterns
        "overlay",
        "caption",
        "scribble",
        "graphic",
        # Social media
        "social",
        "post",
        "tweet",
        "story",
        "reel"
    ]
    
    # Preferred domains - Clean stock photos + Reuters/AFP (wire photos are usually clean)
    PREFERRED_DOMAINS = [
        # Wire services - usually clean
        "reuters.com",
        "apnews.com", 
        "afp.com",
        # Stock agencies
        "gettyimages.com",
        "gettyimages.in",
        "gettyimages.co.uk",
        "imagoimages.com",
        "imago-images.de",
        "sportsphoto.com",
        "profimedia.si",
        # ESPN player photos (usually clean portraits)
        "espncricinfo.com/players",
        "espncricinfo.com/photo",
        "a.espncricinfo.com",
    ]
    
    def is_acceptable_image(url: str) -> bool:
        """Check if image is from acceptable domain and not text/thumbnail."""
        url_lower = url.lower()
        
        # Must end with valid image extension
        if not any(url_lower.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
            return False
        
        # Check if from excluded domain
        for domain in EXCLUDED_DOMAINS:
            if domain in url_lower:
                return False
        
        # Check for excluded patterns (text, thumbnails, quotes, etc.)
        for pattern in EXCLUDED_PATTERNS:
            if pattern in url_lower:
                return False
        
        return True
    
    def get_domain_priority(url: str) -> int:
        """Lower number = higher priority."""
        url_lower = url.lower()
        for i, domain in enumerate(PREFERRED_DOMAINS):
            if domain in url_lower:
                return i
        return len(PREFERRED_DOMAINS)  # Default lowest priority
    
    if not TAVILY_API_KEY:
        logger.warning("No Tavily API key, using fallback")
        return FALLBACK_URL
    
    try:
        # Use Tavily client for search
        from tavily import TavilyClient
        
        tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
        
        # Search for images related to the prompt
        search_results = tavily_client.search(
            query=prompt,
            max_results=10,
            include_images=True
        )
        
        # Collect all acceptable images
        acceptable_images = []
        
        # Extract image URLs from results
        if search_results.get("images"):
            for img_url in search_results["images"]:
                if is_acceptable_image(img_url):
                    acceptable_images.append(img_url)
        
        # If no images in search, try to get from results
        if search_results.get("results") and not acceptable_images:
            for result in search_results["results"]:
                if "img" in result or "image" in result:
                    img_url = result.get("img") or result.get("image")
                    if is_acceptable_image(img_url):
                        acceptable_images.append(img_url)
        
        # Sort by domain priority (preferred domains first)
        if acceptable_images:
            acceptable_images.sort(key=get_domain_priority)
            logger.info(f"🟢 [SUCCESS] Image found via Tavily: {acceptable_images[0][:50]}...")
            return acceptable_images[0]
        
        logger.warning("No acceptable images found in Tavily search results")
        
    except ImportError:
        logger.warning("tavily-python not installed, trying direct API call")
        try:
            # Direct API call fallback
            url = "https://api.tavily.com/search"
            headers = {"Content-Type": "application/json"}
            payload = {
                "api_key": TAVILY_API_KEY,
                "query": prompt,
                "max_results": 10,
                "include_images": True
            }
            
            response = requests.post(url, json=payload, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                acceptable_images = []
                if data.get("images"):
                    for img_url in data["images"]:
                        if is_acceptable_image(img_url):
                            acceptable_images.append(img_url)
                
                if acceptable_images:
                    acceptable_images.sort(key=get_domain_priority)
                    logger.info(f"🟢 [SUCCESS] Image found via Tavily API: {acceptable_images[0][:50]}...")
                    return acceptable_images[0]
                            
        except Exception as e:
            logger.warning(f"Tavily direct API call failed: {e}")
    
    except Exception as e:
        logger.warning(f"Error with Tavily search: {e}")
    
    # Fallback
    logger.warning("Tavily search failed, using fallback image")
    return FALLBACK_URL


def fetch_image_from_prompt(headline: str, detailed_prompt: str) -> str:
    """
    Generates an image using the detailed prompt from other agents.
    """
    logger.info(f"Generating image for headline: {headline[:50]}...")
    return generate_image(detailed_prompt)