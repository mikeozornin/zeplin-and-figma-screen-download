import os

import requests


def download(url, folder, file_name):
    if not os.path.exists(folder):
        os.mkdir(folder)

    path = os.sep.join([folder_name, file_name])

    with open(path, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
        return (path, file_name)