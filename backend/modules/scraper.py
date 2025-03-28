import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from modules.constraints import  is_valid_video

load_dotenv()

def extractVideoUrls(searchQueries=["Trump"], hashtags=["maga"], max_results=5):
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
        "searchSection": "/video",
        "maxProfilesPerQuery": 5,
        "shouldDownloadVideos": False,
        "proxyCountryCode": "US"
    }

    # Run API
    try:
        run = client.actor("OtzYfK1ndEGdwWFKQ").call(run_input=run_input)
    except Exception as e:
        print("Error running actor:", str(e))
        exit(1)

    object={}
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        object[item.get("webVideoUrl")]= {
            'musicId':item["musicMeta"]["musicId"],
            'duration':item["videoMeta"]["duration"], 
            'followers':item["authorMeta"]["fans"],
            'hashtags':[ x["name"] for x in item["hashtags"]],
            'views':item["playCount"],
            "metadata":item
            }
        
    validUrls=[]
    for videoUrl in object:
        if is_valid_video(videoUrl,object[videoUrl]):
            validUrls.append(videoUrl)
    
    return validUrls


if __name__ == "__main__":
    test_queries = ["AI technology", "future of robotics"]
    urls = extractVideoUrls(test_queries, max_results=3)
    print("\nExtracted TikTok Video URLs:", urls)