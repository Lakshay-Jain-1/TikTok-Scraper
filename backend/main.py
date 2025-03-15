from modules.scrapper import extractVideoUrls
from modules.downloader import batch_download
from modules.merge import merging


"""
Documentation 

Function
extractVideoUrls -> return a list of video url's eg ['https://www.tiktok.com/@pich.solikah/video/7481208166252891412']
    has two parmeters
    first parameter
    searchQueries -> it should be a list of string eg ["Trump"]
    second parameter
    hashtags -> it should be a list of string eg ["fyp"]
    third parameter
    max_results (int): Maximum number of video links to retrieve per search.

    
in second phase
run this command winget install ffmpeg

"""

def main(searchQueries, hashtags, max_results):
    # 1st phase
    print("Fetching TikTok video URLs...")
    video_urls = extractVideoUrls(searchQueries, hashtags, max_results)
    
    # 2nd phase
    if video_urls:
        print(f"Extracted {len(video_urls)} videos.")
        batch_download(video_urls)

        # 3rd phase
        merging()
    else:
        print("No videos found.")
        raise Exception("No videos Found")
    

if __name__ == "__main__":
    main()