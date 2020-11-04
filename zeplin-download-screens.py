import json
import sys
import requests
import logging
import time
import os

from common import download, get_image_folder_name
from config import ZEPLIN_API_TOKEN

logging.basicConfig(
    format='Date-Time : %(asctime)s : Line No. : %(lineno)d : Function Name : %(funcName)s - %(message)s',
    level=logging.ERROR)

ZEPLIN_API_URL_BASE = 'https://api.zeplin.dev/v1/'

CHECKPOINT_FILE_NAME = 'zeplin-checkpoint.txt'

ZEPLIN_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(ZEPLIN_API_TOKEN)
}


def get_checkpoint():
    with open(CHECKPOINT_FILE_NAME, 'r') as file:
        checkpoint = file.read()
        return int(checkpoint)


def init_checkpoint():
    yesterday = datetime.date.today() - datetime.timedelta(1)
    print(yesterday.strftime("%s"))


def set_checkpoint():
    with open(CHECKPOINT_FILE_NAME, 'w+') as file:
        file.write(str(round(time.time())))


# Получаем список проектов
def get_projects():
    api_url = '{0}projects?limit=100'.format(ZEPLIN_API_URL_BASE)

    response = requests.get(api_url, headers=ZEPLIN_HEADERS)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        logging.error(
            f'The function was unable to get data: {response.content.decode("utf-8")}'
        )
        sys.exit(1)


def get_screens_from_zeplin(project):
    screen_for_save = []
    i = 1
    while i <= project['number_of_screens']:
        api_url = '{0}projects/{1}/screens?sort=created&limit=100&offset={2}' \
            .format(ZEPLIN_API_URL_BASE, project['id'], i)
        print(f'{project["name"]}: request screens from {i} to {i + 99}')
        response = requests.get(api_url, headers=ZEPLIN_HEADERS)
        if response.status_code == 200:
            screens = json.loads(response.content.decode('utf-8'))
            for screen in screens:
                # print('id: {0}, name: {1}, updated: {2}'.format(screen['id'], screen['name'], screen['updated']))
                screen_for_save.append([{
                    'id': screen['id'],
                    'name': screen['name'],
                    'updated': screen['updated'],
                    'image': screen['image']['original_url']
                }])

            i += 100
        else:
            logging.error(f'The function was unable to get data: {response.content.decode("utf-8")}')
            sys.exit(1)
    return screen_for_save


# Что бы красиво выплюнуть json в консоль
def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(
            json.dumps(json.loads(json_thing),
                       sort_keys=sort,
                       indent=indents,
                       ensure_ascii=False))
    else:
        print(
            json.dumps(json_thing,
                       sort_keys=sort,
                       indent=indents,
                       ensure_ascii=False))
    return None


if __name__ == '__main__':
    # init_checkpoint()                   # uncomment if you want not to download all screens
    checkpoint = get_checkpoint()
    folder_name = get_image_folder_name()

    for project in get_projects():
        if project['status'] != 'active':
            continue
        screens_new = get_screens_from_zeplin(project)
        for item in screens_new:
            screen = item[0]
            if screen['updated'] > checkpoint:
                url = screen['image']
                project_name = project['name'].replace('/', '_').replace('|', '_')
                screen_file_name = '%s__%s' % (project_name, screen['name'].replace('/', '_') + "@2x.png")
                download(url, folder_name, screen_file_name)

    set_checkpoint()
