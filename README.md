# Публикация комиксов во ВКонтакте
Сервис позволяет получать с сайта  [xkcd.com](https://xkcd.com/) случайный комикс и опубликовать его
на стене Сообщества. 

## Как работает
Запустите файл publish_comic.py в виртуальном окружении. Программа скачивает случайный комикс во 
временную папку, публикует его на стене сообщества, после чего удаляет скачанный файл из папки.
По умолчанию, название папки  ``images``, но его можно задать, используя необязательный аргумент ``-f`` 
или ``--folder``.

### Как установить

* Python3 должен уже быть установлен.
* Для изоляции проекта рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html).
* Чтобы развернуть зависимости, используйте **`pip`** (или **`pip3`**, если есть конфликт с Python2):
```bash
$ pip install -r requirements.txt
```

### Авторизация
1. Создайте файл **``.env``**, в котором будете сохранят переменные **``VK_ACCESS_TOKEN``**, 
**``VK_API_VERSION``**, **``CLIENT_ID``**, **``GROUP_ID``** (обязательно со знаком ``минус``).
Например:
```python
VK_ACCESS_TOKEN=vk1.a.hJkYApCRcrywymQhmaG2w8ZqCvu3rsYVXMhqg6R
VK_API_VERSION=5.131
GROUP_ID=-123456789
CLIENT_ID=51587816
```
2. Создайте группу Вконтакте, в которую будете выкладывать комиксы. В адресе сообщества будет указан его id.
Например: https://vk.com/club219380486, где 219380486 - id, который нужно будет сохранить в файле .env в переменной 
GROUP_ID со знаком ``минус``.
3. Для постинга на стену нужен ключ доступа пользователя. Чтобы его получить, 
создайте ``standalone``-приложение на странице Вконтакте [для разработчиков](https://vk.com/dev).
4. В разделе 'настройки' приложения получите ID приложения, запишите его в переменную **``CLIENT_ID``**.
5. Получите ключ доступа пользователя, который нужен для доступа к вашему аккаунту и публикации сообщения в группах. 
Чтобы получить ключ, воспользуйтесь процедурой [Implicit Flow](https://vk.com/dev/implicit_flow_user).
Запрос токен для предоставления доступа выглядит следующим образом: 
https://oauth.vk.com/authorize?client_id=<CLIENT_ID>&display=page&scope=photos,groups,wall,offline&response_type=token&v=<VK_API_VERSION>
При получении ключа вы увидите страницу со списком разрешений как на скриншоте.

![image](https://i.paste.pics/MIVPN.png)

После чего получите ссылку, содержащую токен. Токен сохраните в переменную **``VK_ACCESS_TOKEN``**.

### Примеры
Для получения справки используйте аргумент ```-h``` или ```--help```.

```bash
$ python publish_comic.py --help
```
Вывод:
```
usage: publish_comic.py [-h] [-f FOLDER]

Публикация случайного комикса на стене сообщества в VK

options:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        Ввести название временного каталога
```

Примеры запросов:
```bash
$ python publish_comic.py
```

или

```bash
$ python publish_comic.py -f temp
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).

### Лицензия

Этот проект лицензирован по лицензии MIT - подробности см. в файле [ЛИЦЕНЗИЯ](LICENSE).
