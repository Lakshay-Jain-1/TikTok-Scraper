import requests

NEWS_KEYWORDS = ["news", "breaking", "politics", "report", "update", "headline","c4news","Channel 4 News"]

def is_valid_video(videoUrl,metadata):
    # Check view Count
    if int(metadata["views"])>2000000:
        print(metadata["views"])
        print("Got rejected as view count was more than 2 million")
        return False
    
    # Check music (Is it copyright or not ?)
    if  music_check_copyright(metadata["musicId"]):     
        return False
    
    # Check if duration is greater than 8 minutes
    if int(metadata["duration"])>480:
        return False
    
    # Check if video is of news cateogry
    for i in metadata["hashtags"]:
        if i in NEWS_KEYWORDS:
            return False
    if is_news_video(metadata["metadata"]):
        return False

    return True

def music_check_copyright(musicID):
    root = "https://ensembledata.com/apis"
    endpoint = "/tt/music/details"
    params = {
        "id": musicID,
        "token": "vchHlG3DctoKgfPW"
    }
    
    try:
        res = requests.get(root + endpoint, params=params)
        res.raise_for_status()  # Raise an exception for HTTP errors
        data = res.json().get("data", {})
        # Return True if commercial_right_type equals 2, else False
        return data.get("commercial_right_type") == 2
    except requests.RequestException as e:
        print("Request failed:", e)
        return False
    except ValueError as e:
        print("Invalid JSON:", e)
        return False

def is_news_video(metadata):
    # Check if any hashtag is in NEWS_KEYWORDS
    for hashtag in metadata.get("hashtags", []):
        if any(keyword in hashtag["name"].lower() for keyword in NEWS_KEYWORDS):
            return True

    # Check if any author metadata field contains a NEWS_KEYWORD
    for key, value in metadata.get("authorMeta", {}).items():
        if isinstance(value, str) and any(keyword in value.lower() for keyword in NEWS_KEYWORDS):
            return True

    return False