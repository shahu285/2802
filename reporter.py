import logging
import requests
import xml.etree.ElementTree as ET

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
    # High-credibility, free feeds for Football (Sky Sports) and Cricket (ESPN Cricinfo)
    rss_targets = {
        "Cricket Feed": "https://www.espncricinfo.com/rss/content/story/feeds/6.xml",
        "Football Feed": "https://www.skysports.com/rss/12040"
    }
    
    all_discovered_articles = []
    
    logger.info("Starting automated sweep across sports media horizons...")
    
    for feed_name, url in rss_targets.items():
        try:
            logger.info(f"Connecting to data target: {feed_name}")
            
            # Send an HTTP request to pull the raw XML feed data
            response = requests.get(url, timeout=10)
            
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
                    
                    if title is not None:
                        article_data = {
                            "source": feed_name,
                            "headline": title.text.strip(),
                            "url": link.text.strip() if link is not None else "No URL found"
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
    
    print("\n--- 📢 AGENT EXPERIMENTAL DISCOVERY OUTPUT ---")
    for index, article in enumerate(headlines[:5], 1): # Print just the top 5 articles to keep terminal clean
        print(f"{index}. [{article['source']}] {article['headline']}")
    print("-----------------------------------------------\n")
    
    logger.info("Local developer validation cycle complete.")