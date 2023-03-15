import os
import requests



def main():
    pass


if __name__ == '__main__':
    # main()

    images_path = 'files'
    os.makedirs(images_path, exist_ok=True)

    link = 'https://xkcd.com/info.0.json'  # /info.0.json

    response = requests.get(url=link)
    response.raise_for_status()
    comic = response.json()
    print(comic['img'])
