import os
import requests
from tqdm import tqdm
from rich.console import Console
import threading
import tkinter as tk
import platform
import vlc
from dotenv import load_dotenv

load_dotenv()

console = Console()
API_TOKEN = os.getenv('DOWNLOAD_TIKTOK_API_TOKEN')

# RapidAPI credentials and endpoint
API_URL = "https://tiktok-video-downloader-api.p.rapidapi.com/media"
HEADERS = {
    "x-rapidapi-key": str(API_TOKEN),
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
        play_video_and_get_feedback(filepath)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading video: {e}")

def play_video_and_get_feedback(filepath):
    """VLC video player implementation with automatic setup"""
    root = tk.Tk()
    root.title("Video Preview")
    root.geometry("400x300+100+100")

    video_frame = tk.Frame(root, bg="black")
    video_frame.pack(fill=tk.BOTH, expand=True)

    # Configure VLC with platform-specific optimizations
    vlc_options = [
        '--quiet',
        '--no-osd',
        '--avcodec-hw=any',
        '--drop-late-frames',
        '--skip-frames'
    ]

    instance = vlc.Instance(*vlc_options)
    player = instance.media_player_new()
    media = instance.media_new(filepath)
    player.set_media(media)

    # Windows-specific window handling
    if platform.system() == "Windows":
        win_id = video_frame.winfo_id()
        player.set_hwnd(win_id)
    else:  # Linux/macOS
        player.set_xwindow(video_frame.winfo_id())

    player.play()

    # Playback monitoring
    stop_event = threading.Event()

    def check_playback():
        if stop_event.is_set() or player.get_state() == vlc.State.Ended:
            root.quit()
        else:
            root.after(100, check_playback)

    print("Press Enter in terminal to stop playback...")
    
    # Input handling thread
    def wait_for_enter():
        input()
        player.stop()
        stop_event.set()

    threading.Thread(target=wait_for_enter, daemon=True).start()
    root.after(100, check_playback)
    root.mainloop()

    # Cleanup
    player.release()
    root.destroy()

    # User feedback
    choice = input("Accept video? (y/n): ").lower()
    if choice == 'y':
        print("Video accepted.")
    else:
        try:
            os.remove(filepath)
            print("Video deleted.")
        except Exception as e:
            print(f"Deletion error: {e}")

def batch_download(video_urls):
    """Downloads multiple TikTok videos from a list of URLs."""
    for idx, video_url in enumerate(video_urls, start=1):
        ## For testing purposes
        # if idx==4:
        #     console.print(
        #         "To reduce the testing duration, only three videos will be downloaded",
        #         style="bold white on blue" 
        #     )
        #     break
        print(f"\n Processing Video {idx}/{len(video_urls)}: {video_url}")
        download_url = get_download_url(video_url)
        if download_url:
            filename = f"tiktok_video_{idx}.mp4"
            download_tiktok_video(download_url, filename)
        else:
            print(f"⚠️ Skipping video {idx} due to an error.")