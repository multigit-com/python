import sys
sys.path.append('../')
from function.folder_exist import folder_exist
import os



def non_git_folders_in_path(path_folder):
    files = os.listdir(path_folder)
    # print(files)
    folders = []
    for file in files:
        current_path = os.path.join(path_folder, file)
        if folder_exist(current_path + "/" + ".git"):
            print(f"GIT Exist: {current_path}")
        else:
            folders.append(f"{current_path}")
    return folders