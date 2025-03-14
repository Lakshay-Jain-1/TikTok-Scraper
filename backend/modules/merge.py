import os
import subprocess

DOWNLOADS_FOLDER = "downloads"
OUTPUT_FOLDER = "converted_videos"
MERGED_FILE = "final_merged.mp4"

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def convert_to_h264():
    """
    Converts all MP4 files in the downloads folder to H.264 format.
    """
    converted_files = []
    
    for filename in os.listdir(DOWNLOADS_FOLDER):
        if filename.endswith(".mp4"):
            input_path = os.path.join(DOWNLOADS_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(filename)[0]}_h264.mp4")
            
            # FFmpeg command to convert to H.264
            command = [
                "ffmpeg", "-i", input_path, "-c:v", "libx264", "-crf", "23", "-preset", "fast",
                "-c:a", "aac", "-b:a", "192k", output_path, "-y"
            ]
            
            print(f"Converting {filename} to H.264...")
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            converted_files.append(output_path)
    
    return converted_files

def merge_videos(converted_files):
    """
    Merges all converted H.264 videos into a single file.
    """
    if not converted_files:
        print("No converted videos found for merging.")
        return

    # Create a text file with list of videos
    file_list = os.path.join(OUTPUT_FOLDER, "file_list.txt")
    with open(file_list, "w") as f:
        for video in converted_files:
            f.write(f"file '{video}'\n")

    merged_output = os.path.join(OUTPUT_FOLDER, MERGED_FILE)

    # FFmpeg command to merge videos
    merge_command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", file_list, "-c", "copy", merged_output, "-y"]
    
    print("Merging videos...")
    subprocess.run(merge_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Merging complete! Final file: {merged_output}")

if __name__ == "__main__":
    converted_videos = convert_to_h264()
    merge_videos(converted_videos)
