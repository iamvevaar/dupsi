
import os
import hashlib
import shutil
from tqdm import tqdm

def calculate_hash(file_path):
    """Calculate the MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicate_files(folder1, folder2, duplicate_folder):
    """Find and move duplicate files from two folders to a duplicate_folder."""
    # Dictionary to store file hashes and paths
    file_hashes = {}

    # Get the total number of files to process for the progress bar
    total_files = sum(len(files) for _, _, files in os.walk(folder1)) + sum(len(files) for _, _, files in os.walk(folder2))

    # Create a progress bar
    with tqdm(total=total_files, desc="Progress", unit="file") as pbar:
        # Iterate through folder1
        for root, _, files in os.walk(folder1):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_hash = calculate_hash(file_path)
                if file_hash in file_hashes:
                    duplicate_file_path = file_hashes[file_hash]
                    move_file(file_path, duplicate_file_path, duplicate_folder)
                else:
                    file_hashes[file_hash] = file_path
                pbar.update(1)  # Update the progress bar

        # Iterate through folder2
        for root, _, files in os.walk(folder2):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_hash = calculate_hash(file_path)
                if file_hash in file_hashes:
                    duplicate_file_path = file_hashes[file_hash]
                    move_file(file_path, duplicate_file_path, duplicate_folder)
                else:
                    file_hashes[file_hash] = file_path
                pbar.update(1)  # Update the progress bar

def move_file(src, duplicate_src, duplicate_folder):
    """Move duplicate file to the duplicate_folder."""
    print(f"Moving duplicate file: {src}")
    shutil.move(src, os.path.join(duplicate_folder, os.path.basename(duplicate_src)))

if __name__ == "__main__":
    folder1_path = r"E:\Backup\NOTE 10 COMPLETE\DCIM\After"
    folder2_path = r"E:\Backup\NOTE 10 COMPLETE\DCIM\FS"
    duplicate_folder_path = r"E:\Backup\NOTE 10 COMPLETE\DCIM\Duplicate Folder"

    find_duplicate_files(folder1_path, folder2_path, duplicate_folder_path)
