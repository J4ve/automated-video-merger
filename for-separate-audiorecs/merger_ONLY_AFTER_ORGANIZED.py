import os
import subprocess

# Get script's directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths
video_dir = os.path.join(base_dir, "Videos")
audio_dir = os.path.join(base_dir, "Audio")
output_dir = os.path.join(base_dir, "OUTPUT")

# Create OUTPUT folder if it doesn’t exist
os.makedirs(output_dir, exist_ok=True)

# 🔹 Merge Video + Audio
for video in os.listdir(video_dir):
    name, ext = os.path.splitext(video)
    
    if ext.lower() != ".mp4":
        continue  # Skip non-video files

    merged_video_path = os.path.join(output_dir, f"{name}_merged.mp4")
    
    # ✅ Skip if already merged
    if os.path.exists(merged_video_path):
        print(f"✅ {name}_merged.mp4 already exists, skipping...")
        continue

    video_path = os.path.join(video_dir, video)
    audio_path = os.path.join(audio_dir, f"{name}.m4a")  # Match audio file
    
    if not os.path.exists(audio_path):
        print(f"❌ No matching audio for {video}, skipping...")
        continue

    # FFmpeg command to mix both audios (video + external)
    command = [
        "ffmpeg", "-hwaccel", "cuda",
        "-i", video_path, "-i", audio_path, 
        "-filter_complex", "[0:a:0][1:a:0]amix=inputs=2:duration=first[aout]",
        "-map", "0:v:0", "-map", "[aout]",
        "-c:v", "h264_nvenc", "-preset", "fast", "-cq", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        merged_video_path
    ]

    print(f"🚀 Merging: {video} + {name}.m4a (Stacking Audio)")
    subprocess.run(command)

print("✅ All videos processed successfully! Now run the second script to batch merge them.")
