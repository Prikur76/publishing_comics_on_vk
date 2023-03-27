import argparse
import logging
import os
from random import choice
from urllib.parse import urljoin, urlsplit, unquote

import requests
from dotenv import load_dotenv

import vk_upload_photo as vk

logger = logging.getLogger(__name__)

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
    comic_number = choice(range(1, comics_count, 1))
    xkcd_random_url = f'https://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(url=xkcd_random_url)
    response.raise_for_status()
    comic = response.json()
    image = urlsplit(comic['img'])
    image_name = os.path.split(
        unquote(image.path, encoding='utf-8', errors='replace')
    )
    comic_description = [comic['img'], comic['alt'], image_name[1]]
    return comic_description


def fetch_image_from_url(image_link, image_directory, image_name):
    """Скачивает картинку с интернета по ссылке (GET-запрос)"""
    response = requests.get(url=image_link)
    response.raise_for_status()
    image_path = os.path.join(
        os.path.abspath(image_directory), image_name
    )
    with open(image_path, 'wb') as file:
        file.write(response.content)


def main():
    logging.basicConfig(
        format='[%(levelname)s] - %(asctime)s - %(name)s - %(message)s',
        level=logging.INFO
    )

    load_dotenv()

    vk_token = os.environ['VK_ACCESS_TOKEN']
    vk_api_version = os.environ['VK_API_VERSION']
    group_id = os.environ['GROUP_ID']

    parser = argparse.ArgumentParser(
        description='Публикация случайного комикса на стене сообщества в VK'
    )
    parser.add_argument('-f', '--folder', default='images',
                        help='Ввести название временного каталога')
    args = parser.parse_args()
    images_path = os.path.abspath(args.folder)

    if not os.path.exists(images_path):
        os.makedirs(images_path)

    try:
        comic = get_random_comic_description()
        comic_url, comic_alt, comic_name = comic
        comic_path = os.path.join(images_path, comic_name)

        fetch_image_from_url(
            comic_url, images_path, comic_name
        )

        attachments = vk.get_attachments_for_publish(
            vk_token, vk_api_version, group_id, comic_path
        )

        vk.publish_photo_on_wall(
            vk_token, vk_api_version, group_id,
            attachments, message=comic_alt
        )
        os.remove(comic_path)

    except requests.exceptions.HTTPError as http_err:
        logger.error(f'Request failed with HTTPError: {http_err}')

    except OSError as os_err:
        logger.error(f'Failed with OSError: {os_err.comic_path}')


if __name__ == '__main__':
    main()
