from apify_client import ApifyClient
import time

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_7Na9Qlv8BaFyHzrkWXF25N1bY76hzj07Xpuv")

# Function to check if a video meets the required criteria
def is_valid_video(video):
    print("\nChecking Video:", video.get("webVideoUrl", "No URL"))
    print("Duration:", video.get("duration", "Unknown"))
    print("Music Metadata:", video.get("musicMeta", {}).get("musicName"))
    
    # Debugging: Temporarily remove the music filter and increase duration limit
    return (
        video.get("duration", 0) <= 600  # Increased to 10 min for testing
        # and video.get("musicMeta", {}).get("musicName") is None  # Temporarily disabled
    )

# Function to check if a profile meets the criteria
def is_valid_profile(profile):
    print("\nChecking Profile:", profile.get("username", "Unknown"))
    print("Follower Count:", profile.get("stats", {}).get("followerCount", 0))
    print("User Type:", profile.get("userType", "Unknown"))
    
    return (
        profile.get("stats", {}).get("followerCount", 0) < 2_000_000
        and profile.get("userType") != "news"
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
    "proxyCountryCode": "US"
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
