# from apify_client import ApifyClient

# # Initialize the ApifyClient with your API token
# client = ApifyClient("apify_api_4f6p8I6Np9mpTHzMfdMCmLnwKALyPx2Sgl2s")

# # Prepare the Actor input
# run_input = {
#     "hashtags": ["fyp"],
#     "resultsPerPage": 100,
#     "profileScrapeSections": ["videos"],
#     "profileSorting": "latest",
#     "excludePinnedPosts": False,
#     "searchQueries": [
#         "New innovations in solar and wind energy"
#     ],
#     "searchSection": "/video",
#     "maxProfilesPerQuery": 10,
#     "shouldDownloadVideos": False,
#     "shouldDownloadCovers": False,
#     "shouldDownloadSubtitles": False,
#     "shouldDownloadSlideshowImages": False,
# }

# # Run the Actor and wait for it to finish
# run = client.actor("OtzYfK1ndEGdwWFKQ").call(run_input=run_input)

# # Fetch and print Actor results from the run's dataset (if there are any)
# def is_usa_user(user_id):
#     """Check if a TikTok user ID matches the common USA pattern."""
#     return user_id.startswith("67") or user_id.startswith("68")

# for item in client.dataset(run["defaultDatasetId"]).iterate_items():
#     if "id" in item and is_usa_user(item["id"]):
#         print(item)




# from apify_client import ApifyClient

# # Initialize the ApifyClient with your API token
# client = ApifyClient("apify_api_dvWeQGo0BOAJDS05l3Idr376atadX02xinZg")

# # Function to check if a user is from the USA based on their user ID pattern
# def is_usa_user(user_id):
#     return str(user_id).startswith(("67", "68"))  # Example pattern for US users

# # Function to check if the video meets the required criteria
# def is_valid_video(video):
#     return (
#         video.get("musicMetadata") is None or not video["musicMetadata"].get("title")  # No music
#         and video.get("duration", 0) <= 480  # Max 8 min (480 sec)
#     )

# # Function to check if a profile meets the criteria
# def is_valid_profile(profile):
#     return (
#         is_usa_user(profile.get("id", ""))  # USA user
#         and profile.get("stats", {}).get("followerCount", 0) < 2_000_000  # Under 2M followers
#         and profile.get("userType") != "news"  # Not a news organization
#     )

# # Prepare the Actor input
# run_input = {
#     "hashtags": ["fyp"],
#     "resultsPerPage": 30,
#     "profileScrapeSections": ["videos"],
#     "profileSorting": "latest",
#     "excludePinnedPosts": False,
#     "searchQueries": [
#         "New innovations in solar and wind energy"
#     ],
#     "searchSection": "/video",
#     "maxProfilesPerQuery": 20,
#     "shouldDownloadVideos": False,
#     "shouldDownloadCovers": False,
#     "shouldDownloadSubtitles": False,
#     "shouldDownloadSlideshowImages": False,
# }

# # Run the Actor and wait for it to finish
# run = client.actor("OtzYfK1ndEGdwWFKQ").call(run_input=run_input)

# # Fetch and filter results
# for item in client.dataset(run["defaultDatasetId"]).iterate_items():
#     profile = item.get("author", {})
#     videos = item.get("videos", [])

#     if is_valid_profile(profile):
#         filtered_videos = [video for video in videos if is_valid_video(video)]
        
#         if filtered_videos:
#             print({
#                 "username": profile.get("username"),
#                 "followers": profile.get("stats", {}).get("followerCount"),
#                 "videos": [
#                     {
#                         "id": video.get("id"),
#                         "description": video.get("desc"),
#                         "duration": video.get("duration"),
#                         "likes": video.get("stats", {}).get("diggCount"),
#                         "comments": video.get("stats", {}).get("commentCount"),
#                         "shares": video.get("stats", {}).get("shareCount"),
#                     }
#                     for video in filtered_videos
#                 ],
#             })




# from apify_client import ApifyClient

# # Initialize the ApifyClient with your API token
# client = ApifyClient("apify_api_dvWeQGo0BOAJDS05l3Idr376atadX02xinZg")

# # Function to check if a user is from the USA based on their user ID pattern
# def is_usa_user(user_id):
#     return str(user_id).startswith(("67", "68"))  # Example pattern for US users

# # Function to check if the video meets the required criteria
# def is_valid_video(video):
#     return (
#         video.get("musicMetadata") is None or not video["musicMetadata"].get("title")  # No music
#         and video.get("duration", 0) <= 480  # Max 8 min (480 sec)
#     )

# # Function to check if a profile meets the criteria
# def is_valid_profile(profile):
#     return (
#         is_usa_user(profile.get("id", ""))  # USA user
#         and profile.get("stats", {}).get("followerCount", 0) < 2_000_000  # Under 2M followers
#         and profile.get("userType") != "news"  # Not a news organization
#     )

# # Limit for displayed results
# max_results = 10
# results_count = 0  # Counter for displayed results

# # Prepare the Actor input
# run_input = {
#     "hashtags": ["fyp"],
#     "resultsPerPage": 5,
#     "profileScrapeSections": ["videos"],
#     "profileSorting": "latest",
#     "excludePinnedPosts": False,
#     "searchQueries": [
#         "New innovations in solar and wind energy"
#     ],
#     "searchSection": "/video",
#     "maxProfilesPerQuery": 5,
#     "shouldDownloadVideos": False,
#     "shouldDownloadCovers": False,
#     "shouldDownloadSubtitles": False,
#     "shouldDownloadSlideshowImages": False,
# }

# # Run the Actor and wait for it to finish
# run = client.actor("OtzYfK1ndEGdwWFKQ").call(run_input=run_input)

# # Fetch and filter results
# for item in client.dataset(run["defaultDatasetId"]).iterate_items():
#     # print("Raw Item:", item)  # Debugging: Print all raw data
#     if results_count >= max_results:
#         break  # Stop when limit is reached

#     profile = item.get("author", {})
#     videos = item.get("videos", [])

#     if is_valid_profile(profile):
#         filtered_videos = [video for video in videos if is_valid_video(video)]
        
#         if filtered_videos:
#             print({
#                 "username": profile.get("username"),
#                 "followers": profile.get("stats", {}).get("followerCount"),
#                 "videos": [
#                     {
#                         "id": video.get("id"),
#                         "description": video.get("desc"),
#                         "duration": video.get("duration"),
#                         "likes": video.get("stats", {}).get("diggCount"),
#                         "comments": video.get("stats", {}).get("commentCount"),
#                         "shares": video.get("stats", {}).get("shareCount"),
#                         "url": video.get("videoUrl")  # Assuming the URL is stored in the 'videoUrl' field
#                     }
#                     for video in filtered_videos
#                 ],
#             })
#             results_count += 1  # Increment result counter





from apify_client import ApifyClient
import time

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_dvWeQGo0BOAJDS05l3Idr376atadX02xinZg")

# Prepare the Actor input
run_input = {
    "hashtags": ["fyp"],
    "resultsPerPage": 5,
    "profileScrapeSections": ["videos"],
    "profileSorting": "latest",
    "excludePinnedPosts": False,
    "searchQueries": ["New innovations in solar and wind energy"],
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

# Fetch and store all video URLs
video_urls = []

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    video_url = item.get("webVideoUrl")
    if video_url:
        video_urls.append(video_url)

# Print all video URLs
print("\nAll Video URLs:")
for url in video_urls:
    print(url)
