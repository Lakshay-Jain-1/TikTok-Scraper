from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_QSbJy3rWtd34pKSRdJg7H1r2MSlD4j2Lq8KO")

# Prepare the Actor input
run_input = {
    "excludePinnedPosts": False,
    "hashtags": ["fyp"],
    "maxProfilesPerQuery": 20,
    "proxyCountryCode": "US",
    "resultsPerPage": 100,
    "searchQueries": ["Trump"],
    "searchSection": "/video",
    "shouldDownloadAvatars": False,
    "shouldDownloadCovers": False,
    "shouldDownloadMusicCovers": False,
    "shouldDownloadSlideshowImages": False,
    "shouldDownloadSubtitles": False,
    "shouldDownloadVideos": False,
}

# Run the Actor and wait for it to finish
run = client.actor("GdWCkxBtKWOsKjdch").call(run_input=run_input)

# Check if the actor ran successfully
if run["status"] != "SUCCEEDED":
    print(f"Actor failed with status: {run['status']}")
    exit(1)

# Fetch and print Actor results
dataset_client = client.dataset(run["defaultDatasetId"])
for item in dataset_client.iterate_items():
    print(item)