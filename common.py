import os
import requests
import datetime


BASE_FOLDER = 'images'


def download(url, folder, file_name):
    if not os.path.exists(folder):
        os.mkdir(folder)

    path = os.sep.join([folder, file_name])

    with open(path, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
        return (path, file_name)

def get_image_folder_name():
    if not os.path.exists(BASE_FOLDER):
        os.mkdir(BASE_FOLDER)

    today = datetime.date.today()
    return os.sep.join([BASE_FOLDER, today.isoformat()])