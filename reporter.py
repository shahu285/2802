import logging
import random
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

# =====================================================================
# 🪵 SYSTEM LOGGING CONFIGURATION (Our Mandatory Safeguard)
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (Node: %(name)s) -> %(message)s",
    handlers=[
        logging.FileHandler("newsroom.log"),  # Permanently writes logs to a file
        logging.StreamHandler()               # Simultaneously prints logs to your terminal
    ]
)

# Instantiate our isolated node logger
logger = logging.getLogger("Beat_Reporter")

# =====================================================================
# 🏎️ THE INGESTION ENGINE
# =====================================================================
def fetch_major_headlines():
    """
    Connects to verified sports RSS streams and extracts the latest 
    published article headlines and summaries.
    """
    # High-credibility, free feeds for Football (Sky Sports), Cricket (ESPN Cricinfo), All News, and Other Sports (NDTV)
    rss_targets = {
        "Cricket Feed": "https://www.espncricinfo.com/rss/content/story/feeds/6.xml",
        "Football Feed": "https://www.skysports.com/rss/12040",
        "All News Feed": "https://sports.ndtv.com/rss/all",
        "Other Sports Feed": "https://sports.ndtv.com/rss/othersports"
    }
    
    all_discovered_articles = []
    
    logger.info("Starting automated sweep across sports media horizons...")
    
    for feed_name, url in rss_targets.items():
        try:
            logger.info(f"Connecting to data target: {feed_name}")
            
            # Send an HTTP request to pull the raw XML feed data
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(url, timeout=10, headers=headers)
            
            if response.status_code == 200:
                logger.info(f"Connection successful (Status 200) for {feed_name}. Parsing structural elements...")
                
                # Parse the raw XML text structure
                root = ET.fromstring(response.content)
                
                # Every standard RSS feed houses articles inside an <item> tag
                articles_found = root.findall(".//item")
                logger.info(f"Extracted {len(articles_found)} recent articles from {feed_name}.")
                
                # Loop through the articles and pull out the title data
                for item in articles_found:
                    title = item.find("title")
                    link = item.find("link")
                    pub_date = item.find("pubDate")
                    
                    # Parse publication date if available
                    article_date = None
                    if pub_date is not None and pub_date.text:
                        try:
                            article_date = parsedate_to_datetime(pub_date.text)
                        except Exception:
                            pass
                    
                    if title is not None:
                        article_data = {
                            "source": feed_name,
                            "headline": title.text.strip(),
                            "url": link.text.strip() if link is not None else "No URL found",
                            "pub_date": article_date
                        }
                        all_discovered_articles.append(article_data)
            else:
                logger.warning(f"Target server responded with an error code: {response.status_code} for {feed_name}")
                
        except Exception as e:
            # If the internet drops or a link times out, our engine catches the error and keeps running
            logger.error(f"Critical connection block encountered while reading {feed_name}: {e}")
            
    return all_discovered_articles

# =====================================================================
# 🚀 LOCAL VALIDATION RUN
# =====================================================================
if __name__ == "__main__":
    logger.info("Executing local developer test run...")
    
    headlines = fetch_major_headlines()
    
    # Filter articles older than 24 hours
    cutoff_time = datetime.now().replace(tzinfo=None) - timedelta(hours=24)
    recent_headlines = [
        article for article in headlines 
        if article.get("pub_date") 
        and article["pub_date"].replace(tzinfo=None) > cutoff_time
    ]
    
    # Group by feed/category
    categories = {}
    for article in recent_headlines:
        source = article["source"]
        if source not in categories:
            categories[source] = []
        categories[source].append(article)
    
    # Shuffle within each category (keep date order within category)
    for cat in categories:
        random.shuffle(categories[cat])
    
    # Interleave articles from each category for variety
    shuffled_headlines = []
    max_len = max(len(cat) for cat in categories.values()) if categories else 0
    for i in range(max_len):
        for cat in categories:
            if i < len(categories[cat]):
                shuffled_headlines.append(categories[cat][i])
    
    print("\n--- 📢 AGENT EXPERIMENTAL DISCOVERY OUTPUT ---")
    for index, article in enumerate(shuffled_headlines[:6], 1):  # Print top 6 articles
        print(f"{index}. [{article['source']}] {article['headline']}")
    print("-----------------------------------------------\n")
    
    logger.info("Local developer validation cycle complete.")