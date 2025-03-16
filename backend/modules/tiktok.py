from apify_client import ApifyClient
import time

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_dvWeQGo0BOAJDS05l3Idr376atadX02xinZg")

# Function to check if a video meets the required criteria
def is_valid_video(video):
    return (
        video.get("duration", 0) <= 480  # Max 8 min (480 sec)
        and video.get("musicMeta", {}).get("musicName") is None  # No copyright music
    )

# Function to check if a profile meets the criteria
def is_valid_profile(profile):
    return (
        profile.get("stats", {}).get("followerCount", 0) < 2_000_000  # Under 2M followers
        and profile.get("userType") != "news"  # Not a news organization
    )

# Limit for displayed results
max_results = 10
results_count = 0  # Counter for displayed results

# Prepare the Actor input
run_input = {
    "hashtags": ["fyp"],
    "resultsPerPage": 5,
    "profileScrapeSections": ["videos"],
    "profileSorting": "latest",
    "excludePinnedPosts": False,
    "searchQueries": [
        "New innovations in solar and wind energy"
    ],
    "searchSection": "/video",
    "maxProfilesPerQuery": 5,
    "shouldDownloadVideos": False,
    "shouldDownloadCovers": False,
    "shouldDownloadSubtitles": False,
    "shouldDownloadSlideshowImages": False,
    "proxyCountryCode": "None"
}

# Run the Actor and get the run ID
run = client.actor("OtzYfK1ndEGdwWFKQ").call(run_input=run_input)

# Wait for the actor to finish processing
while True:
    run_status = client.run(run["id"]).get()

    if run_status and "status" in run_status:
        status = run_status["status"]
        print(f"Actor Status: {status}")  # Print status updates

        if status in ["SUCCEEDED", "FAILED", "TIMED_OUT"]:
            break  # Exit when actor finishes

    time.sleep(5)  # Wait 5 seconds before checking again

# Lists to store video URLs
all_video_urls = []      # Stores all returned URLs
filtered_video_urls = [] # Stores only valid (filtered) URLs

# Fetch and filter results
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    # Extract the video URL
    video_url = item.get("webVideoUrl", "")

    # Store all video URLs before filtering
    if video_url:
        all_video_urls.append(video_url)

    # Check if we have enough filtered results
    if results_count >= max_results:
        break

    profile = item.get("authorMeta", {})
    videos = [item]  # Since each item itself is a video

    # Check if the profile is valid
    if is_valid_profile(profile):
        # Filter videos based on the criteria
        filtered_videos = [video for video in videos if is_valid_video(video)]

        # Collect the URLs of filtered videos
        for video in filtered_videos:
            filtered_video_urls.append(video.get("webVideoUrl"))
            results_count += 1

# Display all video URLs
print("\nAll Video URLs:")
for url in all_video_urls:
    print(url)

# Display only filtered video URLs
print("\nFiltered Video URLs (After Applying Criteria):")
for url in filtered_video_urls:
    print(url)
