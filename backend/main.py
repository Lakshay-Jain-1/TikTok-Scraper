from modules.scraper import extractVideoUrls
from modules.downloader import batch_download
from modules.merge import merging ,count_videos_in_downloads
from modules.query_hashtag_refiner import refine_query_and_hashtags
from rich.console import Console

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
    max_results (int): Maximum number of pages will it scrap to retrieve per search.

    

"""

def main(searchQueries, hashtags, max_results):
    use_gemini = input("\nDo you want to use Gemini AI for refining the query and hashtags? (y/n): ").strip().lower() 
    # 0th phase Refining Queries
    if use_gemini == "y":
        searchQueries,hashtags = refine_query_and_hashtags(searchQueries,hashtags)
        print("Refined Queries",searchQueries)
        print("Refined Hashtags",hashtags)

    # 1st phase (To fetch tik tok URL's)
    print("Fetching TikTok video URLs...")
    video_urls = extractVideoUrls(searchQueries, hashtags, max_results)
            
    if len(video_urls) == 0:
        print("No TikTok URLs found. Exiting the program. Please try running the code again.")
        exit()

    # 2nd phase (To download videos using tik tok url's)
    if video_urls:
        print(f"Extracted {len(video_urls)} videos.")
        batch_download(video_urls)
        
        Console.print(f"Manual test complete: {count_videos_in_downloads()} out of {len(video_urls)} videos downloaded successfully.", style="bold yellow")

        # Phase 3: Ask user if they want to merge the downloaded videos
        user_input = input("Do you want to merge the videos currently in the Downloads folder? Type 'y' for yes or 'n' for no: ")
        if user_input.lower() == "y":
            merging()
            
    else:
        print("No videos found.")
        raise Exception("No videos found to process.")

    print("The process is now complete.")


if __name__ == "__main__":
    main(searchQueries=["Trump"], hashtags=["maga"], max_results=5)
