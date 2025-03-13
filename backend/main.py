from modules.scrapper import extractVideoUrls
from modules.downloader import download_videos



"""
Documentation 

Function
extractVideoUrls -> return a list of video url's eg ['https://www.tiktok.com/@pich.solikah/video/7481208166252891412']
    has two parmeters
    first parameter
    searchQueries -> it should be a list of string eg ["Trump"]
    second parameter
    hashtags -> it should be a list of string eg ["fyp"]

    
in second phase
run this command winget install ffmpeg



"""

def main():
    # 1st phase
    print("Fetching TikTok video URLs...")
    video_urls = extractVideoUrls()
    
    # 2nd phase
    if video_urls:
        print(f"Extracted {len(video_urls)} videos.")
        
        # Call the downloader function
        download_videos(video_urls)
    else:
        print("No videos found.")
    
    # 3rd phase
    

if __name__ == "__main__":
    main()






