import os
import requests
from tqdm import tqdm
from rich.console import Console
import threading
import tkinter as tk
import platform
import vlc
from dotenv import load_dotenv
import shutil
import hashlib
load_dotenv()

console = Console()
API_TOKEN = os.getenv('DOWNLOAD_TIKTOK_API_TOKEN')

# RapidAPI configuration
API_URL = "https://tiktok-video-downloader-api.p.rapidapi.com/media"
HEADERS = {
    "x-rapidapi-key": str(API_TOKEN),
    "x-rapidapi-host": "tiktok-video-downloader-api.p.rapidapi.com"
}

DOWNLOAD_FOLDER = "downloads"
HISTORY_FOLDER = "history"

# Create downloads folder if it doesn't exist
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Check for video files in downloads folder
video_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm')
video_files = []
for filename in os.listdir(DOWNLOAD_FOLDER):
    if os.path.splitext(filename)[1].lower() in video_extensions:
        video_files.append(os.path.join(DOWNLOAD_FOLDER, filename))

# Move videos to history folder if any exist
if video_files:
    # Create history folder if needed
    os.makedirs(HISTORY_FOLDER, exist_ok=True)
    
    # Move files with duplicate handling
    moved_count = 0
    for src_path in video_files:
        filename = os.path.basename(src_path)
        base, ext = os.path.splitext(filename)
        dest_path = os.path.join(HISTORY_FOLDER, filename)
        
        # Handle existing files by appending a number
        counter = 1
        while os.path.exists(dest_path):
            new_filename = f"{base}_{counter}{ext}"
            dest_path = os.path.join(HISTORY_FOLDER, new_filename)
            counter += 1
        
        shutil.move(src_path, dest_path)
        moved_count += 1

    print(f"Moved {moved_count} video(s) to {HISTORY_FOLDER}")
else:
    print("No videos found in downloads folder")

class VideoPlayer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.player = None
        self.instance = None
        self.player_active = False
        self.stop_event = threading.Event()
        self.root = None
        self.input_thread = None
        self.console = Console()

    def play(self):
        """Initialize and start video playback"""
        try:
            # Create Tkinter root window
            self.root = tk.Tk()
            self.root.title("Video Preview")
            self.root.geometry("800x600+100+100")
            self.root.protocol("WM_DELETE_WINDOW", self.safe_shutdown)

            # Video frame setup
            video_frame = tk.Frame(self.root, bg="black")
            video_frame.pack(fill=tk.BOTH, expand=True)

            # VLC initialization
            self.init_vlc(video_frame)
            
            # Start playback monitoring
            self.start_playback()
            
            # Start input handling
            self.start_input_handler()
            
            # Show instructions
            self.console.print("Click in this terminal window first, then press Enter to stop playback..", style="bold yellow")
            
            # Main loop
            self.root.mainloop()

        except Exception as e:
            self.console.print(f"🚨 Playback error: {e}", style="bold red")
        finally:
            self.cleanup()

    def init_vlc(self, video_frame):
        """Initialize VLC media player"""
        vlc_options = [
            '--quiet',
            '--no-osd',
            '--avcodec-hw=any',
            '--drop-late-frames',
            '--skip-frames'
        ]
        
        self.instance = vlc.Instance(*vlc_options)
        self.player = self.instance.media_player_new()
        media = self.instance.media_new(self.filepath)
        self.player.set_media(media)

        # Platform-specific window handling
        if platform.system() == "Windows":
            self.player.set_hwnd(video_frame.winfo_id())
        else:
            self.player.set_xwindow(video_frame.winfo_id())

        self.player.play()
        self.player_active = True

    def start_playback(self):
        """Start playback monitoring"""
        def check_playback():
            if self.stop_event.is_set() or not self.player_active:
                return
            
            try:
                state = self.player.get_state()
                if state in [vlc.State.Ended, vlc.State.Stopped, vlc.State.Error]:
                    self.safe_shutdown()
                else:
                    self.root.after(100, check_playback)
            except Exception as e:
                self.console.print(f"🚨 State check error: {e}", style="bold red")
                self.safe_shutdown()

        self.root.after(100, check_playback)

    def start_input_handler(self):
        """Handle terminal input with proper synchronization"""
        def input_listener():
            try:
                input()  # Wait for Enter press
                self.root.after(0, self.safe_shutdown)
            except Exception as e:
                self.console.print(f"🚨 Input error: {e}", style="bold red")

        self.input_thread = threading.Thread(target=input_listener, daemon=True)
        self.input_thread.start()

    def safe_shutdown(self):
        """Thread-safe shutdown procedure"""
        if self.player_active:
            try:
                self.player.stop()
                self.stop_event.set()
                self.player_active = False
                self.root.after(100, self.root.quit)
            except Exception as e:
                self.console.print(f"🚨 Shutdown error: {e}", style="bold red")

    def cleanup(self):
        """Resource cleanup"""
        try:
            if self.player:
                self.player.release()
            if self.instance:
                self.instance.release()
            if self.root:
                self.root.destroy()
        except Exception as e:
            self.console.print(f"🚨 Cleanup error: {e}", style="bold red")

def handle_user_feedback(filepath):
    """Get user decision with timeout"""
    try:
        # Use readchar to avoid threading issues with input()
        import readchar
        print("Accept video? (y/n): ", end="", flush=True)
        char = readchar.readchar().lower()
        print(char)  # Echo the input
        
        if char != 'y':
            os.remove(filepath)
            console.print("🗑️ Video deleted", style="bold yellow")
        else:
            console.print("👍 Video accepted", style="bold green")
    except Exception as e:
        console.print(f"❌ Feedback error: {e}", style="bold red")

def get_download_url(video_url):
    """Fetch download URL from API"""
    try:
        response = requests.get(
            API_URL,
            headers=HEADERS,
            params={"videoUrl": video_url},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("downloadUrl")
    except Exception as e:
        console.print(f"❌ API Error: {e}", style="bold red")
        return None

def download_video(download_url, filename):
    """Download video with progress bar"""
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    try:
        with requests.get(download_url, stream=True, timeout=15) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
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
                
            
            console.print(f"✅ Download complete: {filepath}", style="bold green")
            return filepath
    except Exception as e:
        console.print(f" Download failed: {e}", style="bold red")
        # Clean up incomplete file if exists
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                console.print(f"🗑️ Deleted incomplete file: {filepath}", style="bold yellow")
            except Exception as delete_error:
                console.print(f"❌ Failed to delete file: {delete_error}", style="bold red")
        return None


def process_video(video_url, index):
    """Full processing pipeline for a single video"""
    console.print("\nPlease DO NOT type or press Enter while the video is downloading. Just follow the instructions.", style="bold red")
    console.print(f"Processing Video {index}: {video_url}", style="bold blue")
    
    if download_url := get_download_url(video_url):
        hashed_url = hashlib.md5(video_url.encode()).hexdigest()
        filename = f"tiktok_video_{hashed_url}_{index}.mp4"
        if filepath := download_video(download_url, filename):
            console.print(" Starting playback...", style="bold yellow")
            VideoPlayer(filepath).play()
            handle_user_feedback(filepath)

def batch_download(video_urls):
    """Process multiple videos with proper error handling"""
    for index, url in enumerate(video_urls, start=1):
        try:
            process_video(url, index)
        except Exception as e:
            console.print(f" Skipping video {index} due to error: {e}", style="bold red")
            continue

if __name__ == "__main__":
    # Example usage
    test_urls = [
        "https://www.tiktok.com/@amusingmichele/video/7491477001946025221",
        "https://www.tiktok.com/@voteinorout/video/7489981612159946014"
    ]
    
    batch_download(test_urls)