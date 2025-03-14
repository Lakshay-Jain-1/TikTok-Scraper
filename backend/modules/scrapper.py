import os
import time
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load environment variables
load_dotenv()

def extractVideoUrls(searchQueries=["AI technology"], hashtags=["fyp"], max_results=5):
    """
    Uses Apify TikTok Scraper to extract video URLs based on search queries and hashtags.
    
    Parameters:
        searchQueries (list): Keywords to search for TikTok videos.
        hashtags (list): List of hashtags to filter videos.
        max_results (int): Maximum number of video links to retrieve per search.

    Returns:
        list: A list of extracted TikTok video URLs.
    """

    # Get API token from environment
    API_TOKEN = os.getenv('TIKTOK_SCRAPPER_API_TOKEN')
    if not API_TOKEN:
        raise ValueError("API token not found! Set the TIKTOK_SCRAPPER_API_TOKEN environment variable.")

    # Initialize Apify Client
    client = ApifyClient(API_TOKEN)

    # Define search parameters
    run_input = {
        "hashtags": hashtags,
        "resultsPerPage": max_results,
        "profileScrapeSections": ["videos"],
        "profileSorting": "latest",
        "excludePinnedPosts": False,
        "searchQueries": searchQueries, 
        "searchSection": "",  
        "maxProfilesPerQuery": 3,  
        "shouldDownloadVideos": False,
        "shouldDownloadCovers": False,
        "shouldDownloadSubtitles": False,
        "shouldDownloadSlideshowImages": False,
        "shouldDownloadAvatars": False,
        "shouldDownloadMusicCovers": False,
        "proxyCountryCode": "None",
    }

    # Start the actor
    print("Starting TikTok scraping process...")
    run = client.actor("GdWCkxBtKWOsKjdch").call(run_input=run_input)

    # Wait for the results to be ready
    time.sleep(5)  

    # Fetch and extract video URLs from Apify dataset
    video_urls = []
    dataset = client.dataset(run["defaultDatasetId"])
    
    print("Fetching results from Apify...")
    
    for item in dataset.iterate_items():
        if "webVideoUrl" in item:
            video_urls.append(item["webVideoUrl"])

    if video_urls:
        print(f"Extracted {len(video_urls)} video URLs.")
    else:
        print("No videos found. Check Apify logs for issues.")

    return video_urls


if __name__ == "__main__":
    test_queries = ["AI technology", "future of robotics"]
    urls = extractVideoUrls(test_queries, max_results=3)
    print("\nExtracted TikTok Video URLs:", urls)