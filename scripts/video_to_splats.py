import subprocess
import os

def extract_frames(video_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-i", video_path,
        f"{output_path}/frame_%05d.png"
    ]
    subprocess.run(cmd, check=True)