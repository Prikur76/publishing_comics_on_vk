import os
from urllib.parse import urljoin

from dotenv import load_dotenv

import requests



def get_groups_info(base_url, vk_token, vk_api_version):
    """ """
    method = 'groups.get'
    params = {
        'extended': 1,
        'access_token': vk_token,
        'v': vk_api_version,
    }
    group_url = urljoin(base_url, method)

    response = requests.get(url=group_url, params=params)
    response.raise_for_status()

    full_info = response.json()['response']
    groups_count, groups_descriptions = full_info['count'], full_info['items']

    return groups_count, groups_descriptions


def get_wall_upload_server(base_url, vk_token, vk_api_version):
    """ """
    wall_upload_method = 'photos.getWallUploadServer'
    payload = {
        'access_token': vk_token,
        'v': vk_api_version,
    }
    wall_upload_url = urljoin(base_url, wall_upload_method)
    response = requests.get(url=wall_upload_url, params=payload)
    upload_server_info = response.json()['response']
    album_id, upload_url, user_id = upload_server_info.values()
    return abs(album_id), upload_url, user_id


def upload_photo(upload_url, photo_path):
    """ """
    with open(photo_path, 'rb') as file:
        files = {
            'photo': file,
        }
    response = requests.post(url=upload_url, files=files)
    response.raise_for_status()
    upload_response = response.json()
    return upload_response


def save_wall_photo(base_url, vk_token, vk_api_version, upload_response):
    """ """
    save_wall_method = 'photos.saveWallPhoto'
    save_wall_url = urljoin(base_url, save_wall_method)
    server, photo, hash = upload_response.values()
    payload = {
        'access_token': vk_token,
        'v': vk_api_version,
        'server': server,
        'photo': photo,
        'hash': hash,
    }
    response = requests.post(url=save_wall_url, data=payload)
    response.raise_for_status()
    photos_descriptions_for_publishing = response.json()['response']
    attachments = []
    for photo in photos_descriptions_for_publishing:
        album_id = photo['album_id']
        media_id = photo['id']
        owner_id = photo['owner_id']
        attachment = f'photo{owner_id}_{media_id}'
        attachments.append(attachment)
    return attachments


def publish_photo_on_wall(vk_token, vk_api_version, group_id,
                          attachments, message='', friends_only=0,
                          from_group=1):
    """
    Публикует изображение на странице сообщества и
    возвращает ID поста
    """

    wall_post_method = 'wall.post'
    wall_post_url = urljoin(base_url, wall_post_method)
    payload = {
        'access_token': vk_token,
        'v': vk_api_version,
        'owner_id': group_id,
        'friends_only': 0,
        'from_group': 1,
        'message': comic_alt,
        'attachments': attachments,
    }
    response = requests.post(url=wall_post_url, data=payload)
    response.raise_for_status()
    post_id = response.json()['response']
    return post_id.values()



load_dotenv()

vk_token = os.getenv('VK_ACCESS_TOKEN')
vk_api_version = os.getenv('VK_API_VERSION')
vk_user_id = os.getenv('VK_USER_ID')
base_url = 'https://api.vk.com/method/'
group_id = os.getenv('GROUP_ID')

photo_name = 'lymphocytes.png'

# groups = get_groups_info(base_url)[1]
# print(*groups)

wall_upload_info = get_wall_upload_server(base_url, vk_token, vk_api_version)
upload_url = wall_upload_info[1]
# print(album_id, upload_url, user_id)
with open('images/' + photo_name, 'rb') as file:
    files = {
        'photo': file,
    }
    response = requests.post(url=upload_url, files=files)
    response.raise_for_status()
upload_response = response.json()

method = 'photos.saveWallPhoto'
save_wall_url = urljoin(base_url, method)
server, photo_description, hash = upload_response.values()
payload = {
    'access_token': vk_token,
    'v': vk_api_version,
    'server': server,
    'photo': photo_description,
    'hash': hash,
}
response = requests.post(url=save_wall_url, data=payload)
response.raise_for_status()
photos_descriptions_for_publishing = response.json()['response']

attachments = []
for photo in photos_descriptions_for_publishing:
    album_id = photo['album_id']
    media_id = photo['id']
    owner_id = photo['owner_id']
    attachment =  f'photo{owner_id}_{media_id}'
    attachments.append(attachment)
# print(attachments)

comic_alt = "We'll turn the asteroid belt into ball bearings " \
            "to go between different rings orbiting at different speeds."

print(response.json())

