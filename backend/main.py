# from modules.scrapper import extractVideoUrls

# """
# Documentation 

# Function
# extractVideoUrls -> return a list of video url's eg ['https://www.tiktok.com/@pich.solikah/video/7481208166252891412']
#     has two parmeters
#     first parameter
#     searchQueries -> it should be a list of string eg ["Trump"]
#     second parameter
#     hashtags -> it should be a list of string eg ["fyp"]


# """



# def main():
#     # phase 1 to extract the url's
#     videoUrls =  extractVideoUrls() 
#     print(videoUrls) # it will return video url's

#     # phase 2


# if __name__ == "__main__":
#     main()




from modules.scrapper import extractVideoUrls
from modules.downloader import download_videos


def main():
    print("Fetching TikTok video URLs...")
    video_urls = extractVideoUrls()
    
    if video_urls:
        print(f"Extracted {len(video_urls)} videos.")
        
        # Call the downloader function
        download_videos(video_urls)
    else:
        print("No videos found.")

if __name__ == "__main__":
    main()



