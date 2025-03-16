rom apify_client import ApifyClient
import time

client = ApifyClient("apify_api_7Na9Qlv8BaFyHzrkWXF25N1bY76hzj07Xpuv")

# List of keywords to filter out news-related content
NEWS_KEYWORDS = ["news", "breaking", "politics", "report", "update", "headline"]

def is_valid_video(video):
    video_url = video.get("webVideoUrl", "No URL")
    duration = video.get("videoMeta", {}).get("duration", 0)
    music_name = video.get("musicMeta", {}).get("musicName", "Unknown")
    is_copyrighted = video.get("musicMeta", {}).get("isOriginal", True)

    # Extracting view count from the top level
    view_count = video.get("playCount", 0)
    if view_count is None:
        print(f"❌ ERROR: 'playCount' key missing for {video_url}! Defaulting to 0.")
        view_count = 0
    elif isinstance(view_count, str) and view_count.isdigit():
        view_count = int(view_count)
    elif not isinstance(view_count, int):
        print(f"❌ ERROR: Unexpected data type for 'playCount' in {video_url}! Setting view_count to 0.")
        view_count = 0

    # Process text content safely
    text_content = video.get("text", "")
    if not isinstance(text_content, str):
        print(f"❌ ERROR: text_content for {video_url} is not a string!")
        text_content = ""
    else:
        text_content = text_content.lower()
    
    print(f"DEBUG: text_content value -> {text_content} (type: {type(text_content)})")

    # Process hashtags safely
    raw_hashtags = video.get("hashtags", [])
    hashtags = []

    if isinstance(raw_hashtags, list):
        for tag in raw_hashtags:
            if isinstance(tag, dict) and "name" in tag:
                hashtags.append(tag["name"].lower())
            elif isinstance(tag, str):
                hashtags.append(tag.lower())
    else:
        print(f"❌ ERROR: hashtags is not a list for {video_url}!")

    print(f"DEBUG: Cleaned hashtags -> {hashtags} (type: {type(hashtags)})")

    # Print debug info
    print(f"\nChecking Video: {video_url}")
    print(f"  Duration: {duration} sec")
    print(f"  View Count: {view_count}")
    print(f"  Music Name: {music_name}")
    print(f"  Copyrighted Music: {'Yes' if is_copyrighted else 'No'}")
    print(f"  Hashtags: {hashtags}")

    # Filter conditions
    if duration == 0:
        print("  ❌ Rejected: No duration info.")
        return False
    if duration > 480:
        print("  ❌ Rejected: Video is longer than 8 min.")
        return False
    if view_count == 0:
        print("  ❌ Rejected: No views.")
        return False
    if view_count >= 2_000_000:
        print("  ❌ Rejected: More than 2M views.")
        return False
    if not is_copyrighted:
        print("  ❌ Rejected: Contains copyrighted music.")
        return False
    if isinstance(text_content, str) and any(keyword in text_content for keyword in NEWS_KEYWORDS):
        print("  ❌ Rejected: Contains news-related text.")
        return False
    if any(tag in NEWS_KEYWORDS for tag in hashtags):
        print("  ❌ Rejected: Has news-related hashtags.")
        return False

    return True


def is_valid_profile(profile):
    user_type = profile.get("userType", "")

    # Debugging print
    print(f"DEBUG: userType value -> {user_type} (type: {type(user_type)})")

    if isinstance(user_type, str):  # Ensure it's a string before calling lower()
        return user_type.lower() != "news"
    
    return True  # Default to valid if userType is missing or not a string


# Prepare API input
run_input = {
    "hashtags": ["fyp"],
    "resultsPerPage": 5,
    "profileScrapeSections": ["videos"],
    "profileSorting": "latest",
    "excludePinnedPosts": False,
    "searchQueries": ["New innovations in AI technology"],
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
    for url in filtered_video_urls:
        print(url)
else:
    print("\n⚠️ No videos matched the filter criteria.")
