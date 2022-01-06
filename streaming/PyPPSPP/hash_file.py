from FileUtil import calculate_hash
import os
MEDIA_FORMAT = [".mp4", ".mkv", ".avi"]


def hash_media_folder(path):
    
    for file in os.listdir(path):
        if file.endswith(tuple(MEDIA_FORMAT)):
            print("File: " + file)
            file_hash = calculate_hash(os.path.join(path,file))
            print("Hash: " + str(file_hash))
            
hash_media_folder("../media/")