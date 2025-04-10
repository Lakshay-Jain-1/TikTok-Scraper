from moviepy import VideoFileClip, concatenate_videoclips
from pathlib import Path
import os

def merging():
    # Get the absolute path to the directory where this script is located.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the absolute path to the downloads folder (one level up)
    downloads_folder = os.path.join(script_dir, "..", "downloads")
    
    # List all files in the downloads folder
    downloaded_videos_list = os.listdir(downloads_folder)
    print("Files found:", downloaded_videos_list)
    
    # Create a list of VideoFileClip objects for each video file
    clips = []
    for video_file in downloaded_videos_list:
        # Resolve the absolute path of the video file
        video_path = Path(os.path.join(downloads_folder, video_file)).resolve()
        clip = VideoFileClip(str(video_path))
        clips.append(clip)
    
    if len(clips)==0:
        exit()

    # Concatenate video clips using the "compose" method to handle different resolutions
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # Define the output path for the merged video
    output_path = os.path.join(downloads_folder, "final_clip.mp4")
    
    # Write the final merged video to file
    final_clip.write_videofile(output_path)
    print("Video is merged and saved at:", output_path)

if __name__ == "__main__":
    merging()