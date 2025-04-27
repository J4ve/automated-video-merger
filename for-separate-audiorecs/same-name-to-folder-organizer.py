import os
import shutil

def organize_files(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    file_groups = {}
    for file in files:
        name, ext = os.path.splitext(file)
        if name not in file_groups:
            file_groups[name] = []
        file_groups[name].append(file)
    
    for name, file_list in file_groups.items():
        if len(file_list) > 1:  # Only create a folder if there are multiple files with the same name
            folder_path = os.path.join(directory, name)
            os.makedirs(folder_path, exist_ok=True)
            for file in file_list:
                shutil.move(os.path.join(directory, file), os.path.join(folder_path, file))
    
if __name__ == "__main__":
    folder_path = input("Enter the directory path: ")
    organize_files(folder_path)
    print("Files organized successfully!")
