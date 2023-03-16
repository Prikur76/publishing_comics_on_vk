import os
from random import choice
from urllib.parse import urljoin

import requests


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


def fetch_image_from_url(image_link, image_directory, image_name, params=None):
    """Скачивает картинку с интернета по ссылке (GET-запрос)"""
    if params is None:
        params = {}
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
    response = requests.get(url=image_link, params=params)
    if response.ok:
        with open(os.path.join(os.path.abspath(image_directory),
                               image_name), 'wb') as f:
            f.write(response.content)
    return


def main():
    comic = get_random_comic_description()
    comic_url, comic_alt, comic_name = comic

    images_path = 'images'
    os.makedirs(images_path, exist_ok=True)

    fetch_image_from_url(image_link=comic_url,
                         image_directory=images_path,
                         image_name=comic_name)
    return comic_alt


if __name__ == '__main__':
    main()
