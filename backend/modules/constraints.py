from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv()

CONSTRAINTS_API_KEY=os.getenv("CONSTRAINTS_API_KEY") 

client = ApifyClient(CONSTRAINTS_API_KEY)

PROXIES = {
    "http": "http://apify_proxy_6Kb8fC7W3EhS91CbBkYCqOhJvATN2w3B20gi",
    "https": "http://apify_proxy_6Kb8fC7W3EhS91CbBkYCqOhJvATN2w3B20gi"
}

# Define keywords for filtering
NEWS_KEYWORDS = {"news", "breaking", "update", "politics", "report", "election"}


def is_valid_video(video):
    video_url = video.get("webVideoUrl", "No URL")
    duration = video.get("videoMeta", {}).get("duration", 0)
    music_name = video.get("musicMeta", {}).get("musicName", "Unknown")
    is_copyrighted = video.get("musicMeta", {}).get("isOriginal", True)

    # Extracting view count
    view_count = video.get("playCount", 0)
    if view_count is None:
        print(f"❌ ERROR: 'playCount' missing for {video_url}! Defaulting to 0.")
        view_count = 0
    elif isinstance(view_count, str) and view_count.isdigit():
        view_count = int(view_count)
    elif not isinstance(view_count, int):
        print(f"❌ ERROR: Unexpected 'playCount' type in {video_url}! Setting to 0.")
        view_count = 0

    # Process text content safely
    text_content = video.get("text", "")
    if not isinstance(text_content, str):
        print(f"❌ ERROR: text_content for {video_url} is not a string!")
        text_content = ""
    else:
        text_content = text_content.lower()
    
    print(f"DEBUG: text_content value -> {text_content}")

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

    print(f"DEBUG: Cleaned hashtags -> {hashtags}")

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
    if any(keyword in text_content for keyword in NEWS_KEYWORDS):
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
    
    return True  


