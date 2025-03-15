import os
import requests
from tqdm import tqdm
from rich.console import Console

console = Console()

# RapidAPI credentials and endpoint
API_URL = "https://tiktok-video-downloader-api.p.rapidapi.com/media"
HEADERS = {
    "x-rapidapi-key": "b3cc9a3551msh65998eb88f26cbap163c0cjsnff9c7ca2d8ba",
    "x-rapidapi-host": "tiktok-video-downloader-api.p.rapidapi.com"
}

# Folder to store downloads
DOWNLOAD_FOLDER = "downloads"

# Ensure the downloads folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_download_url(video_url):
    """Fetches the download URL from the RapidAPI endpoint."""
    try:
        response = requests.get(API_URL, headers=HEADERS, params={"videoUrl": video_url})
        response.raise_for_status()
        data = response.json()
        
        if "downloadUrl" in data:
            return data["downloadUrl"]
        else:
            print(f"❌ Download URL not found for: {video_url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching download URL: {e}")
        return None

def download_tiktok_video(download_url, filename):
    """Downloads the TikTok video with a progress bar."""
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get("content-length", 0))
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)  # Save in the 'downloads' folder

        with open(filepath, "wb") as file, tqdm(
            desc=filename,
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
                bar.update(len(chunk))
        
        print(f"Download complete: {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading video: {e}")

def batch_download(video_urls):
    """Downloads multiple TikTok videos from a list of URLs."""
    for idx, video_url in enumerate(video_urls, start=1):
        ## For testing purposes
        if idx==4:
            console.print(
                "To reduce the testing duration, only three videos will be downloaded",
                style="bold white on blue" 
            )
            break
        print(f"\n Processing Video {idx}/{len(video_urls)}: {video_url}")
        download_url = get_download_url(video_url)
        if download_url:
            filename = f"tiktok_video_{idx}.mp4"
            download_tiktok_video(download_url, filename)
        else:
            print(f"⚠️ Skipping video {idx} due to an error.")