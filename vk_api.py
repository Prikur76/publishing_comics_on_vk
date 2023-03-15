import os
from urllib.parse import urljoin

from dotenv import load_dotenv

import requests



def get_groups_info(base_url, vk_token, vk_api_version):
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


load_dotenv()

vk_token = os.getenv('VK_ACCESS_TOKEN')
vk_api_version = os.getenv('VK_API_VERSION')
vk_user_id = os.getenv('VK_USER_ID')
base_url = 'https://api.vk.com/method/'

# groups = get_groups_info(base_url)[1]
# print(*groups)

group_id = 219380486
method = 'photos.getWallUploadServer'
params = {
    'access_token': vk_token,
    'group_id': group_id,
    'v': vk_api_version,
}
wall_upload_url = urljoin(base_url, method)
response = requests.get(url=wall_upload_url, params=params)
upload_server_info = response.json()['response']
# print(upload_server_info)
album_id, upload_url = abs(upload_server_info['album_id']), upload_server_info['upload_url']
print(album_id)
print(upload_url)
