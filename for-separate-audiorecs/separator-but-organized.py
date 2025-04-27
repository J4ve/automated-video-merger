import os
import shutil

def separate_media(directory):
    video_extensions = {".mp4", ".mkv", ".avi", ".mov", ".flv"}
    audio_extensions = {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"}
    
    video_folder = os.path.join(directory, "Videos")
    audio_folder = os.path.join(directory, "Audio")
    os.makedirs(video_folder, exist_ok=True)
    os.makedirs(audio_folder, exist_ok=True)
    
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                _, ext = os.path.splitext(file)
                if ext in video_extensions:
                    shutil.move(file_path, os.path.join(video_folder, file))
                elif ext in audio_extensions:
                    shutil.move(file_path, os.path.join(audio_folder, file))

if __name__ == "__main__":
    folder_path = input("Enter the directory path: ")
    separate_media(folder_path)
    print("Videos and audio clips separated successfully!")
