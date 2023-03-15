import os

import requests


def fetch_image_from_url(image_link, image_directory, image_name, params=None):
    """Скачивает картинку с интернета по ссылке по GET-запросу"""
    if params is None:
        params = {}
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
    response = requests.get(url=image_link, params=params)
    if response.ok:
        with open(os.path.join(os.path.abspath(image_directory), image_name), 'wb') as f:
            f.write(response.content)
    return


def main():
    images_path = './files'
    os.makedirs(images_path, exist_ok=True)

    link = 'https://xkcd.com/info.0.json'  # /info.0.json

    response = requests.get(url=link)
    response.raise_for_status()
    comic = response.json()
    comic_url = comic['img']
    comic_alt = comic['alt']
    comic_name = comic_url.split('/')[-1]
    print(comic_alt)

    fetch_image_from_url(image_link=comic_url,
                         image_directory=images_path,
                         image_name=comic_name,
                         params=None)


if __name__ == '__main__':
    main()
