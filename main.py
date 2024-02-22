import os
import datetime
from winotify import Notification, audio
import schedule
import time

BASE_FOLDER_PATH = 'D:\\jetbrains\\python projects\\file_notifications'  # Change this to your base folder path
TODAY_DATE = datetime.datetime.now().strftime('%Y-%m-%d')
BASE_SUB_FOLDERS = ['folder1', 'folder2', 'folder3']  # Add your sub folders here
SUB_FOLDERS_FILES = {folder: [] for folder in BASE_SUB_FOLDERS}


def check_if_today_folder_exists():
    if not os.path.exists(os.path.join(BASE_FOLDER_PATH, TODAY_DATE)):
        os.mkdir(os.path.join(BASE_FOLDER_PATH, TODAY_DATE))
        create_sub_folders()
    else:
        print('Today\'s Folder already exists')


def create_sub_folders():
    for folder in BASE_SUB_FOLDERS:
        if not os.path.exists(os.path.join(BASE_FOLDER_PATH, TODAY_DATE, folder)):
            os.mkdir(os.path.join(BASE_FOLDER_PATH, TODAY_DATE, folder))
        else:
            print(f'{folder} Sub folder already exists')
    SUB_FOLDERS_FILES = {folder: [] for folder in BASE_SUB_FOLDERS}




# def populate_sub_folders_files():
#     if TODAY_CREATED:
#         return
#
#     else:
#         SUB_FOLDERS_FILES.clear()
#         for folder in BASE_SUB_FOLDERS:
#             SUB_FOLDERS_FILES[folder] = []


def check_for_new_files():
    check_if_today_folder_exists()
    for folder in BASE_SUB_FOLDERS:
        folder_files = []
        for file in os.listdir(os.path.join(BASE_FOLDER_PATH, TODAY_DATE, folder)):
            if file not in SUB_FOLDERS_FILES[folder]:
                send_windows_notification(file, folder)
                print(f'New File {file} found in {folder} folder')
            else:
                print(f'No new files found in {folder} folder')
            folder_files.append(file)

        if SUB_FOLDERS_FILES[folder] != folder_files:
            SUB_FOLDERS_FILES[folder] = folder_files


def send_windows_notification(file_name, folder_name):
    toast = Notification(app_id="New File Added!!",
                         title=f"{folder_name} Folder",
                         msg=f"{file_name} added to {folder_name} folder",
                         icon=f"{BASE_FOLDER_PATH}\\img.png")
    toast.set_audio(audio.SMS, loop=False)
    toast.add_actions(
        label="Open Folder",
        launch=f"{BASE_FOLDER_PATH}\\{TODAY_DATE}\\{folder_name}"
    )

    toast.show()


if __name__ == '__main__':
    schedule.every(1).seconds.do(check_for_new_files)
    while True:
        schedule.run_pending()
        time.sleep(1)
