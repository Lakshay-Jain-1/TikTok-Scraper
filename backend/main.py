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

# def main():
#     # 1st phase
#     print("Fetching TikTok video URLs...")
#     video_urls = extractVideoUrls()
    
#     # 2nd phase
#     if video_urls:
#         print(f"Extracted {len(video_urls)} videos.")
        
#         # Call the downloader function
#         download_videos(video_urls)
#     else:
#         print("No videos found.")
    
#     # 3rd phase
    

# if __name__ == "__main__":
#     main()




from modules.scrapper import extractVideoUrls
from modules.downloader import download_videos
from modules.merge import merge_videos
import os

def main():
    print("Fetching TikTok video URLs...")
    
    # Extract video URLs
    video_urls = extractVideoUrls()
    
    if not video_urls:
        print("No videos found.")
        return [], None

    print(f"Extracted {len(video_urls)} videos.")
    
    # Download videos and get filenames
    downloaded_videos = download_videos(video_urls)

    if not downloaded_videos:
        print("No videos were downloaded.")
        return [], None

    print(f"Downloaded videos: {downloaded_videos}")

    # Merge downloaded videos
    merged_video = merge_videos(downloaded_videos)

    if merged_video:
        print(f"Merged video created: {merged_video}")
    else:
        print("Merging failed.")

    return downloaded_videos, merged_video

if __name__ == "__main__":
    downloaded_videos, merged_video = main()
    print("\nFinal Output:")
    print(f"Downloaded Videos: {downloaded_videos}")
    print(f"Merged Video: {merged_video}")





