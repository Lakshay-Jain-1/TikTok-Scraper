from moviepy import VideoFileClip, concatenate_videoclips
from pathlib import Path
import os

def merging():
    downloded_Videos_List= os.listdir("../downloads")
    for i in range(len(downloded_Videos_List)):
        video_path = Path(f"../downloads/{downloded_Videos_List[i]}").resolve()
        downloded_Videos_List[i] = VideoFileClip(video_path)
    final_clip = concatenate_videoclips(downloded_Videos_List)
    final_clip.write_videofile("../downloads/final_clip.mp4")
    print("Video is merged")
    return 0

if __name__=="main":
    merging()