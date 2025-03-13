import os
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load environment variables
load_dotenv()

def extractVideoUrls(searchQueries=["Trump"],hashtags=["fyp"]):
    # Get API token
    API_TOKEN = os.getenv('TIKTOK_SCRAPPER_API_TOKEN')
    if not API_TOKEN:
        raise ValueError("API token not found! Set the TIKTOK_SCRAPPER_API_TOKEN environment variable.")

    # Initialize the ApifyClient with your API token
    client = ApifyClient(API_TOKEN)

    # Prepare the Actor input
    run_input = {
        "hashtags": hashtags,
        "resultsPerPage": 3,
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


    run = client.actor("GdWCkxBtKWOsKjdch").call(run_input=run_input)

    # Fetch and extract video URLs from the results
    video_urls = []

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        if "webVideoUrl" in item:
            video_urls.append(item["webVideoUrl"])

    return video_urls


