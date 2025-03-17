import os
import time
from dotenv import load_dotenv
from apify_client import ApifyClient
from modules.constraints import is_valid_profile , is_valid_video

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
        "resultsPerPage": 5,
        "profileScrapeSections": ["videos"],
        "profileSorting": "latest",
        "excludePinnedPosts": False,
        "searchQueries": searchQueries,
        "searchSection": "/video",
        "maxProfilesPerQuery": max_results,
        "shouldDownloadVideos": False,
        "proxyCountryCode": "US"
    }

    # Run API
    try:
        run = client.actor("OtzYfK1ndEGdwWFKQ").call(run_input=run_input)
    except Exception as e:
        print("Error running actor:", str(e))
        exit(1)

    # Wait for completion
    while True:
        try:
            run_status = client.run(run["id"]).get()
            if run_status and "status" in run_status:
                status = run_status["status"]
                if status in ["SUCCEEDED", "FAILED", "TIMED_OUT"]:
                    break
            time.sleep(5)
        except Exception as e:
            print("Error fetching actor status:", str(e))
            break

    # Process results
    filtered_video_urls = []
    results_count = 0

    try:
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            video_url = item.get("webVideoUrl", "")

            profile = item.get("authorMeta", {})
            videos = [item]

            print("\n===== Scraped Video Found =====")
            print(f"URL: {video_url}")

            if is_valid_profile(profile):
                filtered_videos = [video for video in videos if is_valid_video(video)]
                for video in filtered_videos:
                    filtered_video_urls.append(video.get("webVideoUrl"))
                    results_count += 1
    except Exception as e:
        print("Error processing dataset:", str(e))

    # Print filtered results
    if filtered_video_urls:
        print("\n✅ Qualified Videos:")
        return filtered_video_urls

if __name__ == "__main__":
    test_queries = ["AI technology", "future of robotics"]
    urls = extractVideoUrls(test_queries, max_results=3)
    print("\nExtracted TikTok Video URLs:", urls)