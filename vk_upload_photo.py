from urllib.parse import urljoin

import requests


def get_user_groups(method_url, params, user_id, extended=1, filter=None):
    """Возвращает список групп пользователя"""
    method = 'groups.get'
    group_url = urljoin(method_url, method)
    adding_params = {
        'user_id': user_id,
        'extended': extended,
    }
    params.update(adding_params)
    if filter:
        params['filter'] = filter
    response = requests.get(url=group_url, params=params)
    response.raise_for_status()
    user_groups = response.json()['response']
    return user_groups


def get_upload_url(method_url, params, group_id):
    """Возвращает ссылку для загрузки файла"""
    wall_upload_method = 'photos.getWallUploadServer'
    wall_upload_url = urljoin(method_url, wall_upload_method)
    params['group_id'] = abs(int(group_id))
    response = requests.get(url=wall_upload_url, params=params)
    response.raise_for_status()
    upload_server = response.json()['response']
    upload_url = upload_server['upload_url']
    return upload_url


def upload_photo(method_url, params, group_id, image_path):
    """Загружает файл на сервер vk"""
    upload_url = get_upload_url(method_url, params, group_id)
    with open(image_path, 'rb') as image_file:
        files = {
            'photo': image_file,
        }
        response = requests.post(url=upload_url, files=files)
        response.raise_for_status()
    return response.json()


def get_attachments(method_url, params, group_id, image_path):
    """Сохраняет файл на стене сообщества"""
    upload_response = upload_photo(method_url, params, group_id, image_path)
    params.update(upload_response)
    save_wall_method = 'photos.saveWallPhoto'
    save_wall_url = urljoin(method_url, save_wall_method)
    response = requests.post(url=save_wall_url, data=params)
    response.raise_for_status()

    attachments = []
    for photo in response.json()['response']:
        attachment = f"photo{photo['owner_id']}_{photo['id']}"
        attachments.append(attachment)

    return attachments


def publish_photo_on_wall(method_url, params, group_id, attachments,
                          friends_only=0, from_group=1, message=None):
    """
    Публикует изображение на странице сообщества и
    возвращает ответ
    """
    wall_post_method = 'wall.post'
    wall_post_url = urljoin(method_url, wall_post_method)
    adding_params = {
        'owner_id': group_id,
        'friends_only': friends_only,
        'from_group': from_group,
        'attachments': attachments,
        'message': message,
    }
    params.update(adding_params)
    response = requests.post(url=wall_post_url, data=params)
    response.raise_for_status()
    post_id = response.json()['response']
    return post_id