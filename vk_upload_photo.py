from urllib.parse import urljoin

import requests


def get_upload_url(vk_token, vk_api_version, group_id):
    """Возвращает ссылку для загрузки файла"""
    method_url = 'https://api.vk.com/method/'
    wall_upload_method = 'photos.getWallUploadServer'
    wall_upload_url = urljoin(method_url, wall_upload_method)
    params = {
        'access_token': vk_token,
        'v': vk_api_version,
        'group_id': abs(int(group_id)),
    }
    response = requests.get(url=wall_upload_url, params=params)
    response.raise_for_status()
    if 'error' in response.json():
        error_msg = response.json()['error']['error_msg']
        raise requests.exceptions.HTTPError(error_msg)
    upload_server = response.json()['response']
    return upload_server['upload_url']


def upload_photo_on_server(vk_token, vk_api_version,
                           group_id, image_path):
    """Загружает файл на сервер vk"""
    upload_url = get_upload_url(vk_token, vk_api_version, group_id)
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            url=upload_url, files={'photo': image_file}
        )
    response.raise_for_status()
    if 'error' in response.json():
        error_msg = response.json()['error']['error_msg']
        raise requests.exceptions.HTTPError(error_msg)
    return response.json()


def save_photo_on_server(vk_token, vk_api_version,
                         group_id, image_path):
    """
    Сохраняет файл на сервере VK и возвращает ответ,
    содержащий объект фото
    """
    upload_params = upload_photo_on_server(
        vk_token, vk_api_version, group_id, image_path
    )
    server, photo, hash = upload_params.values()
    params = {
        'access_token': vk_token,
        'group_id': abs(int(group_id)),
        'server': server,
        'photo': photo,
        'hash': hash,
        'v': vk_api_version,
    }
    method_url = 'https://api.vk.com/method/'
    save_wall_method = 'photos.saveWallPhoto'
    save_wall_url = urljoin(method_url, save_wall_method)
    response = requests.post(url=save_wall_url, data=params)
    response.raise_for_status()
    if 'error' in response.json():
        error_msg = response.json()['error']['error_msg']
        raise requests.exceptions.HTTPError(error_msg)
    return response.json()['response']


def get_attachments_for_publish(vk_token, vk_api_version,
                                group_id, image_path):
    """Возвращает вложения для публикации поста на стене"""
    server_response = save_photo_on_server(
        vk_token, vk_api_version, group_id, image_path
    )
    attachments = []
    for photo in server_response:
        attachment = f"photo{photo['owner_id']}_{photo['id']}"
        attachments.append(attachment)
    return attachments


def publish_photo_on_wall(vk_token, vk_api_version, group_id,
                          attachments, friends_only=0,
                          from_group=1, message=None):
    """
    Публикует изображение на странице сообщества и
    возвращает номер публикации
    """
    method_url = 'https://api.vk.com/method/'
    wall_post_method = 'wall.post'
    wall_post_url = urljoin(method_url, wall_post_method)
    params = {
        'access_token': vk_token,
        'v': vk_api_version,
        'owner_id': group_id,
        'friends_only': friends_only,
        'from_group': from_group,
        'attachments': attachments,
        'message': message,
    }
    response = requests.post(url=wall_post_url, data=params)
    response.raise_for_status()
    if 'error' in response.json():
        error_msg = response.json()['error']['error_msg']
        raise requests.exceptions.HTTPError(error_msg)
    post_id = response.json()['response']
    return post_id
