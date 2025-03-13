import os
import yt_dlp

def download_videos(video_urls, download_folder="downloads"):
    """
    Downloads TikTok videos from a list of URLs.
    """

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Fake browser headers to bypass TikTok's restrictions
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.tiktok.com/'
    }

    # yt-dlp options with headers
    ydl_opts = {
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'format': 'mp4',
        'noplaylist': True,
        'quiet': False,
        'http_headers': headers,  # Pass the browser headers
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in video_urls:
            try:
                print(f"Downloading: {url}")
                ydl.download([url])
                print(f"Downloaded successfully: {url}\n")
            except Exception as e:
                print(f"Failed to download {url}: {e}")

if __name__ == "__main__":
    test_urls = [
        "https://www.tiktok.com/@couriernewsroom/video/7481284755972181294",
        "https://www.tiktok.com/@teamtrump/video/7481284120056794410"
    ]
    download_videos(test_urls)
