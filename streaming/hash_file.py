from FileUtil import calculate_hash
import os

MEDIA_FORMAT = [".mp4", ".mkv", ".avi"]
MEDIA_FOLDER = "../media/"

def hash_media_folder(path):
    roots = []
    for file in os.listdir(path):
        if file.endswith(tuple(MEDIA_FORMAT)):
            print("File: " + file)
            file_hash = calculate_hash(os.path.join(path,file))
            print("Hash: " + str(file_hash))
            roots.append(file_hash)
    return roots


roots = hash_media_folder(MEDIA_FOLDER)
