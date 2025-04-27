import os
import subprocess

# Get script's directory
base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, "OUTPUT")
batch_dir = os.path.join(output_dir, "BATCHES")

# Create BATCHES folder if it doesn’t exist
os.makedirs(batch_dir, exist_ok=True)

# Get list of merged videos
merged_videos = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith("_merged.mp4")]
merged_videos.sort()  # Sort to maintain order

if not merged_videos:
    print("❌ No merged videos found! Run the first script first.")
    exit()

batch_max_duration = 3 * 60 * 60  # 3 hours in seconds
current_batch = []
current_duration = 0
batch_count = 1
processed_batches = []

# 🔹 Create batch list files
for video in merged_videos:
    # Get video duration
    duration_cmd = [
        "ffprobe", "-i", video, "-show_entries", "format=duration",
        "-v", "quiet", "-of", "csv=p=0"
    ]
    duration = float(subprocess.check_output(duration_cmd).decode().strip())

    # If adding this video exceeds set hours, merge the current batch
    if current_duration + duration > batch_max_duration:
        batch_file = os.path.join(batch_dir, f"batch_{batch_count}.txt")
        with open(batch_file, "w") as f:
            for v in current_batch:
                f.write(f"file '{v}'\n")

        # Merge the batch
        batch_output = os.path.join(batch_dir, f"batch_{batch_count}.mp4")
        merge_cmd = [
            "ffmpeg", "-hwaccel", "cuda",
            "-f", "concat", "-safe", "0",
            "-i", batch_file, "-c", "copy", batch_output
        ]
        print(f"🚀 Merging Batch {batch_count} (Up to set Hours)")
        result = subprocess.run(merge_cmd, check=True)

        if result.returncode == 0:  # Verify merge success
            processed_batches.extend(current_batch)  # Mark these videos as processed

        # Reset for next batch
        batch_count += 1
        current_batch = []
        current_duration = 0

    # Add video to batch
    current_batch.append(video)
    current_duration += duration

# Merge the last batch (if any videos remain)
if current_batch:
    batch_file = os.path.join(batch_dir, f"batch_{batch_count}.txt")
    with open(batch_file, "w") as f:
        for v in current_batch:
            f.write(f"file '{v}'\n")

    batch_output = os.path.join(batch_dir, f"batch_{batch_count}.mp4")
    merge_cmd = [
        "ffmpeg", "-hwaccel", "cuda",
        "-f", "concat", "-safe", "0",
        "-i", batch_file, "-c", "copy", batch_output
    ]
    print(f"🚀 Merging Batch {batch_count} (Up to set Hours)")
    result = subprocess.run(merge_cmd, check=True)

    if result.returncode == 0:
        processed_batches.extend(current_batch)

# ✅ Verify before deleting processed files
if processed_batches:
    print("✅ Merging completed. Deleting processed videos...")
    for video in processed_batches:
        os.remove(video)
else:
    print("⚠️ No videos deleted. Merging might have failed.")

print("✅ All batches created successfully!")
