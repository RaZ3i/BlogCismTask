# Тестовое задание

**Реализовать блог со следующими возможностями:**
- создание, изменение и удаление постов
	- создание поста
		- входные данные
			- автор поста
			- тема поста
			- содержимое поста
		- выходные данные
			- успешность выполнения 
	- изменение поста
		- входные данные
			- идентификатор поста
			- автор поста
			- тема поста
			- содержимое поста
		- выходные данные
			- успешность выполнения 
	- удаление поста
		- входные данные
			- идентификатор поста
		- выходные данные
			- успешность выполнения
- отображение постов на странице веб-браузера
- отображение лайков, поставленных конкретному посту
- модификация количества лайков
	- увеличение количества лайков
		- входные данные
			- идентификатор поста
		- выходные данные
			- успешность выполнения
	- уменьшение количества лайков
		- входные данные
			- идентификатор поста
		- выходные данные
			- успешность выполнения
Фронтенд (работа с браузером) реализовывается средствами бэкенда (например, с использованием Jinja)

**Данные в БД должны содержать:**
    - идентификатор поста
    - тему поста
    - содержимое поста
    - количество лайков
    - автора поста
    - дату публикации

**Приветствуется:**
    - реализация дополнительного функционала за пределами указанного ТЗ
    - использование сериализаторов/десериализаторов
    - использование миграций

## Инструкция для запуска в PyCharm

1. Выбрать File -> Project from version control В открывшемся окне вставить в поле URL ссылку на репозиторий (https://github.com/RaZ3i/TestCase.git) В поле Directory выбрать место, куда клонируется репозиторий
2. Создать виртуальное окружение с помощью команды: **_python -m venv venv_**
3. Активровать окружение с помощью команды: **_venv/Scripts/activate_**
4. Установить зависимости с помощью команды: **_pip install -r requirements.txt_**
5. Запустить сервер с помощью команды: **_uvicorn src.main:app --reload --port 8150_**
6. Перейти на страницу для входа по ссылке http://127.0.0.1:8150/pages/authenticate
7. Swagger документация - http://127.0.0.1:8150/docs


<!--
pip install -r requirements.txt - установка зависимостей
(В файле много лишних зависимостей - В ДАЛЬНЕЙШЕМ УБРАТЬ!!!!!!!!!!!!!!!!!!!!)
P.s. когда-нибудь
ОПИСАНЕ API

РАЗДЕЛ АУТЕНТИФИКАЦИИ И РЕГИСТРАЦИИ

Регистрация нового пользователя
POST-метод
http://127.0.0.1:8150/auth/login/
Записывает access_token в cookie
INPUT:
    {
      "username": str,
      "email": str,
      "hash_password": str
    }
OUTPUT:
    {
      "id": int,
      "success": true
    }

Аутентификация пользователя
POST-метод
http://127.0.0.1:8150/auth/login/
Записывает access_token в cookie
INPUT:
    {
    "username": str,
    "password": str
    }
OUTPUT:
    {
      "access_token": str,
      "token_type": str,
      "success": true
    }

Выход
POST-метод
http://127.0.0.1:8150/auth/logout/
Удаляет access_token из cookie
OUTPUT:
    {
    "success": true
    }


РАЗДЕЛ ОПЕРАЦИЙ ПОЛЬЗОВАТЕЛЯ

Создание поста
POST-метод
http://127.0.0.1:8150/profile/create_post/
Принимает access_token из cookie
INPUT:
    {
     "article_theme": str,
     "article_text": str
    }
OUTPUT:
{
  "post_data": {
            "author": str,
            "author_id": int,
            "post_theme": str,
            "post_text": str,
            "created_at": datetime
  },
  "success": true
}

Изменение поста
PATCH-метод
http://127.0.0.1:8150/profile/modify_post/
Принимает access_token из cookie
INPUT:
    {
    "post_id": int,
    "new_text": str
    }
OUTPUT:
    {
     "success": true,
     "mes": str,
     "date_change": datetime
    }

Удаление поста
DELETE-метод
http://127.0.0.1:8150/profile/delete_post/
Принимает access_token из cookie
INPUT:
    "post_id": int
OUTPUT:
    {
      "success": true,
      "mes": str
    }

Лайк/дизлайк поста
PATCH-метод
http://127.0.0.1:8150/profile/like_post/
Принимает access_token из cookie
INPUT:
    "post_id": int
OUTPUT:
    {
      "success": true,
      "mes": str
    }

Получение всех постов
GET-метод
http://127.0.0.1:8150/profile/get_all_posts/
OUTPUT:
    [
      {
        "article_text": str,
        "id": int,
        "article_author_id": int,
        "updated_at": datetime,
        "likes_count": int | null,
        "likes_id_users": [int],
        "article_theme": "str",
        "article_author": "str",
        "created_at": datetime
      },
      ...
    ]

Frontend часть

Страница регистрации
GET-метод
http://127.0.0.1:8150/pages/registration

Страница входа
GET-метод
http://127.0.0.1:8150/pages/authenticate

Домашняя страница
GET-метод
http://127.0.0.1:8150/pages/home_page

Окно создания нового поста
GET-метод
http://127.0.0.1:8150/pages/create_post_window
-->
