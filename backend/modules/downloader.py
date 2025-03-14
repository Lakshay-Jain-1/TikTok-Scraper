import os
import yt_dlp
import time  # Import time module

def download_videos(video_urls, download_folder="downloads"):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.tiktok.com/'
    }

    cookies = "s_v_web_id=YOUR_COOKIE_HERE"

    for index, url in enumerate(video_urls, start=1):
        video_filename = f"video{index}.mp4"
        ydl_opts = {
            'outtmpl': os.path.join(download_folder, video_filename),
            'format': 'mp4',
            'noplaylist': True,
            'quiet': False,
            'http_headers': headers,
            'cookie': cookies,  # Add TikTok session cookies
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                print(f"Downloading: {url} as {video_filename}")
                ydl.download([url])
                print(f"Downloaded successfully: {video_filename}\n")
                time.sleep(5)  # Wait 5 seconds before downloading the next video
            except Exception as e:
                print(f"Failed to download {url}: {e}")
