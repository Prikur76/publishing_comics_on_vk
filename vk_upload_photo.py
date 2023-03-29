from urllib.parse import urljoin

import requests


def get_upload_url(vk_token, vk_api_version, group_id):
    """Возвращает ссылку для загрузки файла"""
    wall_upload_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': vk_token,
        'v': vk_api_version,
        'group_id': group_id,
    }
    response = requests.get(wall_upload_url, params=params)
    response.raise_for_status()
    if 'error' in response.json():
        error_msg = response.json()['error']['error_msg']
        raise requests.exceptions.HTTPError(error_msg)
    upload_server = response.json()['response']
    return upload_server['upload_url']


def get_photo_upload_params(upload_url, image_path):
    """
    Загружает файл на сервер vk и
    возвращает параметры загрузки
    """
    with open(image_path, 'rb') as image_file:
        response = requests.post(upload_url,
                                 files={'photo': image_file})
    response.raise_for_status()
    if 'error' in response.json():
        error_msg = response.json()['error']['error_msg']
        raise requests.exceptions.HTTPError(error_msg)
    return response.json().values()


def save_photo_on_server(vk_token, vk_api_version, group_id, upload_params):
    """
    Сохраняет файл на сервере VK и возвращает ответ,
    содержащий объект фото
    """
    server, photo, hash_value = upload_params
    params = {
        'access_token': vk_token,
        'group_id': group_id,
        'server': server,
        'photo': photo,
        'hash': hash_value,
        'v': vk_api_version,
    }
    save_wall_url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(save_wall_url, data=params)
    response.raise_for_status()
    if 'error' in response.json():
        error_msg = response.json()['error']['error_msg']
        raise requests.exceptions.HTTPError(error_msg)
    return [f"photo{x['owner_id']}_{x['id']}"
            for x in response.json()['response']]


def publish_photo_on_wall(vk_token, vk_api_version, group_id,
                          attachments, friends_only=0,
                          from_group=1, message=None):
    """
    Публикует изображение на странице сообщества и
    возвращает номер публикации
    """
    wall_post_url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': vk_token,
        'v': vk_api_version,
        'owner_id': f'-{group_id}',
        'friends_only': friends_only,
        'from_group': from_group,
        'attachments': attachments,
        'message': message,
    }
    response = requests.post(wall_post_url, data=params)
    response.raise_for_status()
    if 'error' in response.json():
        error_msg = response.json()['error']['error_msg']
        raise requests.exceptions.HTTPError(error_msg)
    post_id = response.json()['response']
    return post_id
