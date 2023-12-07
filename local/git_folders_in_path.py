import sys
sys.path.append('../')
from local.folder_exist import folder_exist
import os


def git_folders_in_path(path_folder):
    files = os.listdir(path_folder)
    folders = []
    for file in files:
        current_path = os.path.join(path_folder, file)
        if folder_exist(current_path + "/" + ".git"):
            folders.append(f"{current_path}")
    return folders