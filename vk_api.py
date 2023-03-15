import os

from dotenv import load_dotenv

import requests


load_dotenv()

vk_token = os.getenv('VK_ACCESS_TOKEN')
vk_api_version = os.getenv('VK_API_VERSION')
vk_user_id = os.getenv('VK_USER_ID')

method = 'groups.get'
params = {
    'extended': 1,
    'access_token': vk_token,
    'v': vk_api_version,
}
# https://api.vk.com/method/{method}?PARAMS&access_token={vk_token}&v={vk_api_version}

group_url = f'https://api.vk.com/method/{method}?
# print(vk_token)

response = requests.get(url=image_link, params=params)