import os
import requests
from tqdm import tqdm
from rich.console import Console
import cv2
import vlc
import time
import threading
import tkinter as tk

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
        play_video_and_get_feedback(filepath)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading video: {e}")

def play_video_and_get_feedback(filepath):
    """
    Plays the downloaded video using VLC for preview (with sound) inside a small Tkinter window.
    Uses a separate thread to wait for the Enter key to stop playback efficiently.
    """
    root = tk.Tk()
    root.title("Video Preview")
    root.geometry("400x300+100+100")

    video_frame = tk.Frame(root, bg="black")
    video_frame.pack(fill=tk.BOTH, expand=1)

    # Initialize VLC with hardware acceleration and performance options
    vlc_options = [
        '--vout=wingdi',
        '--quiet',
        '--verbose=0',
        '--avcodec-hw=any',
        '--no-osd'    ]
    instance = vlc.Instance(*vlc_options)
    player = instance.media_player_new()
    media = instance.media_new(filepath)
    player.set_media(media)

    win_id = video_frame.winfo_id()
    player.set_hwnd(win_id)

    player.play()

    # Wait for playback to start with timeout
    start_time = time.time()
    timeout = 5  # seconds
    while player.get_state() not in [vlc.State.Playing, vlc.State.Opening]:
        time.sleep(0.1)
        if time.time() - start_time > timeout:
            print("Warning: Playback start timeout. Video may not play correctly.")
            break

    print("Playing video preview with sound in a small window.")
    print("Press Enter in the terminal to stop playback and evaluate the video.")

    stop_event = threading.Event()

    def wait_for_enter():
        input()  # Simplified prompt to reduce delay
        player.stop()
        stop_event.set()

    stop_thread = threading.Thread(target=wait_for_enter, daemon=True)
    stop_thread.start()

    # Periodically check stop event in main thread
    def check_stop():
        if stop_event.is_set():
            root.quit()
        else:
            root.after(50, check_stop)  # Check every 50ms for responsiveness

    root.after(50, check_stop)
    root.mainloop()

    # Cleanup resources
    player.stop()
    player.release()
    del player
    del instance
    root.destroy()

    # Get user feedback
    choice = input("Do you accept the video? (y/n): ")
    if choice.lower() == 'y':
        print("Video accepted.")
    else:
        try:
            os.remove(filepath)
            print("Video rejected and file deleted.")
        except Exception as e:
            print(f"Error deleting video file: {e}")

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