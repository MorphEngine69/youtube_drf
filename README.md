# YouTube DRF - приложение для просмотра видеороликов


Сайт создан в учебных и практических целях, не относящиеся к созданию своего плеера, в качестве альтернативы, использована
библиотека django-embed-video, где указывается ссылка на видео с ютуба, которое будет
воспроизводиться, а не локально хранящаяся на сервере. 

<details>
<summary>Изображения сайта</summary>
 
[![][1]][1]
[![][2]][2]
[![][3]][3]
[![][4]][4]
 
[1]: https://imgur.com/3lw6OQf.jpg
[2]: https://imgur.com/yYqkrS8.jpg
[3]: https://imgur.com/AnXoFQW.jpg
[4]: https://imgur.com/UUZZG2V.jpg
 
</details>

---

## Системные требования
```sh
Python 3.9+
Windows/Linux/macOS
```
---

## Установка проекта на Windows

1. Клонировать репозиторий на компьютер и перейти в него из командной строки:
```sh
git clone https://github.com/MorphEngine69/youtube_drf/

cd youtube_drf
```

2. Создать и активировать виртуальное окружение:
```sh
python -m venv env

source venv/Scripts/activate
```

3. Установить зависимости из файла requirements.txt:
```sh
pip install -r requirements.txt
```

4. Выполнить миграции:
```sh
python manage.py migrate
```

5. Запустить проект:
```sh
python manage.py runserver
```
---

## Установка проекта на Linux и macOS

1. Клонировать репозиторий на компьютер и перейти в него из командной строки:
```sh
git clone https://github.com/MorphEngine69/youtube_drf/

cd youtube_drf
```

2. Создать и активировать виртуальное окружение:
```sh
python3 -m venv venv

source env/bin/activate
```

3. Установить зависимости из файла requirements.txt:
```sh
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```

4. Выполнить миграции:
```sh
python3 manage.py migrate
```

5. Запустить проект:
```sh
python3 manage.py runserver
```
## Документация к API проекта:
```sh
http://127.0.0.1:8000/api/v1/
```
Работа и описание запросов:
1. После выполненных миграций, создать аккаунт с помощью:
```sh
1) python manage.py createsuperuser
или
2) http://127.0.0.1:8000/auth/signup/
```
2. Перейти на страницу и получить access JWT токен:
- /api/v1/auth/jwt/create - получить access токен
- /api/v1/auth/jwt/refresh - для восстановления токена
3. Начать работу с API:
- Profile - отвечает за изменение аватарки и даты рождения пользователя.
- Video - отвечает за публикацию/изменение/удаление видеороликов.
- Follow - отвечает за подписку/отписку пользователя на автора канала.
- Comment - отвечает за добавление/изменение/удаление комментариев к видео.
- LikeDislike - отвечает за добавление/изменение/удаление лайков/дизлайков к видео.

Автор [@MorphEngine69](https://github.com/MorphEngine69/)
* система лайков/дизлайков плохо реализована.
* профиль пользователя возможно лучше было бы расширить с помощью наследования
модели AbstractUser.

