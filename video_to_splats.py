import argparse
from datetime import datetime
import imageio
import subprocess
import os
from tqdm import tqdm

def extract_frames(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    reader = imageio.get_reader(video_path)
    total_frames = reader.count_frames()

    print(f"Extracting {total_frames} frames...")

    for i, frame in enumerate(tqdm(reader, total=total_frames, desc="Extracting frames:", unit="frame")):
        imageio.imwrite(f"{output_dir}/frame_{i:05d}.png", frame)


def run_sharp(images_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    images = sorted([f for f in os.listdir(images_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))])

    print(f"Running SHARP on {len(images)} images...")

    for img in tqdm(images, desc="SHARP processing:", unit="image"):
        img_path = os.path.join(images_dir, img)
        cmd = [
            "sharp", "predict",
            "-i", img_path,
            "-o", output_dir
        ]
        subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser(description="Process frames of a video into 3DGS .ply files with SHARP")
    parser.add_argument("--video", required=True, help="Path of input video")
    parser.add_argument("--frames", help="Directory to save extracted frames")
    parser.add_argument("--out", help="Directory to save SHARP outputs")
    
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Use default output directories if none given
    frames_dir = args.frames or f"data/output_frames/{timestamp}"
    out_dir = args.out or f"data/output_gaussians/{timestamp}"

    extract_frames(args.video, frames_dir)
    run_sharp(frames_dir, out_dir)

    print("\nProcessing completed.\n")

if __name__ == "__main__":
    main()

