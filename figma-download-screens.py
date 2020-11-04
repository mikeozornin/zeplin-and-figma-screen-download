import json
import sys
import requests
import logging
import datetime
import os
import hashlib

from common import download
from config import FIGMA_PROJECTS, FIGMA_API_TOKEN, BASE_FOLDER

logging.basicConfig(
    format='Date-Time : %(asctime)s : Line No. : %(lineno)d : Function Name : %(funcName)s - %(message)s',
    level=logging.ERROR)

FIGMA_API_URL_BASE = 'https://api.figma.com/v1/'

CHECKPOINT_FILE_NAME = 'figma-checkpoint.txt'

FIGMA_HEADERS = {'X-FIGMA-TOKEN': '{0}'.format(FIGMA_API_TOKEN)}


def get_image_folder_name():
    if not os.path.exists(BASE_FOLDER):
        os.mkdir(BASE_FOLDER)

    today = datetime.date.today()
    return os.sep.join([BASE_FOLDER, today.isoformat()])


def get_checkpoints():
    checkpoints = set([])
    with open(CHECKPOINT_FILE_NAME, 'r') as file:
        for line in file.readlines():
            checkpoints.add(line.strip())
        return checkpoints


def save_checkpoints(checkpoints):
    with open(CHECKPOINT_FILE_NAME, 'w+') as file:
        file.writelines(['{0}\n'.format(x) for x in checkpoints])


def md5sum(file_name):
    md5_hash = hashlib.md5()
    with open(file_name, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            md5_hash.update(byte_block)
        return md5_hash.hexdigest()


def check_checkpoint(checkpoints, file_path):
    sum = md5sum(file_path)
    if sum in checkpoints:
        os.remove(file_path)
        return checkpoints

    checkpoints.add(sum)
    save_checkpoints(checkpoints)
    return checkpoints


def get_project_frames(project_id, project_name):
    api_url = '{0}files/{1}?depth=2'.format(FIGMA_API_URL_BASE, project_id)

    response = requests.get(api_url, headers=FIGMA_HEADERS)

    if response.status_code == 200:
        project_json = json.loads(response.content.decode('utf-8'))

    frames = []
    for page in project_json['document']['children']:
        page_name = page['name']
        for frame in page['children']:
            if frame['type'] == 'FRAME':
                frames.append({
                    'id': frame["id"],
                    'projectName': project_name,
                    'page_name': page_name,
                    'frame_name': frame["name"]
                })
    return frames


def download_frame(project_id, frame_id, page_name, frame_name, folder_name, scale_ratio=2):
    api_url = '{0}images/{1}?ids={2}&scale=2&format=png'.format(FIGMA_API_URL_BASE, project_id, frame_id)
    file_name = '{0}_{1}_{2}_{3}@2x.png'.format(project_name, page_name, frame_name, frame_id.replace(':', '_'))

    response = requests.get(api_url, headers=FIGMA_HEADERS)

    if response.status_code == 200:
        image_json = json.loads(response.content.decode('utf-8'))
    else:
        logging.error('The function was unable to get data: {response.content.decode("utf-8")}')
        sys.exit(1)

    url = image_json['images'][frame_id]
    if url:
        return download(url, folder_name, file_name)


if __name__ == '__main__':
    folder_name = get_image_folder_name()
    checkpoints = get_checkpoints()

    for projectKey in FIGMA_PROJECTS.keys():
        project_name = projectKey
        project_id = FIGMA_PROJECTS[projectKey]
        frames = get_project_frames(project_id, project_name)
        for frame in frames:
            result = download_frame(projectKey, frame['id'], frame['page_name'],
                                    frame['frame_name'], folder_name)
            print(result)
            if result:
                (file_path, file_name) = result
                if file_path:
                    checkpoints = check_checkpoint(checkpoints, file_path)
    
    save_checkpoints(checkpoints)
