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

def music_check_copyright(music_id):
    url = "https://shazam.p.rapidapi.com/songs/get-details"
    headers = {
        "X-RapidAPI-Key": "b3cc9a3551msh65998eb88f26cbap163c0cjsnff9c7ca2d8ba",
        "X-RapidAPI-Host": "shazam.p.rapidapi.com"
    }

    try:
        response = requests.get(
            url, 
            headers=headers,
            params={"id": music_id, "locale": "en-US"}
        )
        data = response.json()
        return data.get('share', {}).get('snapchat', '') == 'available'
    except:
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