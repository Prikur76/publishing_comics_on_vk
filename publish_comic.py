import os
from random import choice
from urllib.parse import urljoin
import argparse

import requests
from dotenv import load_dotenv

import vk_upload_photo as vk


def get_comics_count():
    """Возвращает количество комиксов"""
    xkcd_url = urljoin('https://xkcd.com/', '/info.0.json')
    response = requests.get(url=xkcd_url)
    response.raise_for_status()
    comic = response.json()
    return comic['num']


def get_random_comic_description():
    """Возвращает url случайного комикса и его текст"""
    comics_count = get_comics_count()
    comic_number = str(choice(range(1, comics_count, 1)))
    xkcd_random_url = f'https://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(url=xkcd_random_url)
    response.raise_for_status()
    comic = response.json()
    comic_description = [comic['img'], comic['alt'],
                         comic['img'].split('/')[-1]]
    return comic_description


def fetch_image_from_url(image_link, image_directory, image_name):
    """Скачивает картинку с интернета по ссылке (GET-запрос)"""
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
    response = requests.get(url=image_link)
    response.raise_for_status()
    if response.ok:
        image_path = os.path.join(os.path.abspath(image_directory), image_name)
        with open(image_path, 'wb') as file:
            file.write(response.content)
    return


def main():
    load_dotenv()
    group_id = os.getenv('GROUP_ID')

    parser = argparse.ArgumentParser(
        description='Публикация случайного комикса на стене сообщества в VK'
    )
    parser.add_argument('-f', '--folder', default='images',
                        help='Ввести название временного каталога')
    args = parser.parse_args()
    images_path = args.folder
    os.makedirs(images_path, exist_ok=True)

    method_url = 'https://api.vk.com/method/'
    params = {
        'access_token': os.getenv('VK_ACCESS_TOKEN'),
        'v': os.getenv('VK_API_VERSION'),
    }
    comic = get_random_comic_description()
    comic_url, comic_alt, comic_name = comic

    fetch_image_from_url(image_link=comic_url,
                         image_directory=images_path,
                         image_name=comic_name)

    comic_path = os.path.join(images_path, comic_name)
    attachments = vk.get_attachments(method_url, params,
                                     group_id, comic_path)
    vk.publish_photo_on_wall(method_url, params, group_id,
                             attachments, message=comic_alt)
    try:
        os.remove(comic_path)
    except OSError as err:
        print('Error: %s - %s.' % (err.comic_path, err.strerror))


if __name__ == '__main__':
    main()
