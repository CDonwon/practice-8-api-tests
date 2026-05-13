# Практическая работа №8

## Описание

Данный проект содержит набор автотестов для проверки API сервиса `https://secby.ru`.

В рамках практической работы были реализованы проверки авторизации, получения токена, отправки токена, получения профиля пользователя и проверки доступа к методам администратора в соответствии с ролью пользователя.


## Проверяемые API-методы

В работе используются следующие методы API:

POST /api/auth/login  
POST /api/auth/verify  
GET /api/profiles/me  
GET /api/profiles/  
GET /api/profiles/{account_id}


## Назначение файлов

`api_client.py` — содержит класс `ApiClient`, который используется для отправки GET и POST запросов к API.

`tests/conftest.py` — содержит общие фикстуры для получения токена пользователя и администратора.

`tests/test_auth.py` — содержит автотесты для проверки авторизации.

`tests/test_user_profile.py` — содержит автотесты для проверки получения профиля пользователя.

`tests/test_admin.py` — содержит автотесты для проверки методов администратора.

`.env.example` — пример файла с переменными окружения.

`requirements.txt` — список зависимостей проекта.

`pytest.ini` — файл конфигурации pytest.

## Установка и запуск

Для выполнения практической работы был создан  проект `API_testing`. В проекте было создано виртуальное окружение Python командой:

python -m venv venv

Далее были установлены необходимые зависимости из файла `requirements.txt`:

pip install -r requirements.txt

Для хранения настроек и тестовых данных был создан файл `.env`. В него были добавлены базовый URL API, логин и пароль тестового пользователя, а также логин и пароль администратора:

BASE_URL=https://secby.ru

USER_LOGIN=
USER_PASSWORD=

ADMIN_LOGIN=
ADMIN_PASSWORD=

Файл `.env` я решил не загружать, так как он содержит данные для авторизации. Вместо него я выгрузил файл `.env.example`, в котором показана структура необходимых переменных окружения.

После настройки проекта автотесты запускались из терминала командой:

pytest -v

Запуск выполнялся из активированного виртуального окружения `venv`.

## Список реализованных тестов

### Авторизация

- Успешная авторизация пользователя.
- Авторизация пользователя с неверным паролем.
- Авторизация без username.
- Авторизация без password.
- Авторизация с пустым username.
- Авторизация с несуществующим пользователем.
- Проверка получения `access_token`.
- Проверка типа токена.

### Профиль пользователя

- Получение профиля авторизованного пользователя.
- Получение профиля без токена.
- Получение профиля с неверным токеном.
- Проверка структуры ответа профиля.
- Проверка username пользователя.
- Проверка роли пользователя.
- Получение профиля пользователя по собственному `account_id`.

### Администратор и ролевая модель

- Получение профиля администратора.
- Проверка роли администратора.
- Получение списка профилей администратором.
- Получение профиля пользователя администратором по `account_id`.
- Запрет получения списка профилей без токена.
- Запрет получения списка профилей с неверным токеном.
- Запрет получения профиля администратора обычным пользователем.

## Пример успешного запуска

После запуска команды:

pytest -v

ожидается успешное прохождение тестов:

collected 17 items

tests/test_admin.py::test_admin_can_get_own_profile PASSED
tests/test_admin.py::test_admin_can_get_profiles_list PASSED
tests/test_admin.py::test_profiles_list_without_token_is_forbidden PASSED
tests/test_admin.py::test_profiles_list_with_invalid_token_is_forbidden PASSED
tests/test_admin.py::test_admin_can_get_user_profile_by_account_id PASSED
tests/test_admin.py::test_user_cannot_get_admin_profile_by_account_id PASSED
tests/test_auth.py::test_user_can_login PASSED
tests/test_auth.py::test_user_cannot_login_with_wrong_password PASSED
tests/test_auth.py::test_login_without_username PASSED
tests/test_auth.py::test_login_without_password PASSED
tests/test_auth.py::test_login_with_empty_username PASSED
tests/test_auth.py::test_login_with_unknown_user PASSED
tests/test_user_profile.py::test_user_can_get_own_profile PASSED
tests/test_user_profile.py::test_user_cannot_get_profile_without_token PASSED
tests/test_user_profile.py::test_user_cannot_get_profile_with_invalid_token PASSED
tests/test_user_profile.py::test_user_profile_response_has_required_fields PASSED
tests/test_user_profile.py::test_user_can_get_profile_by_own_account_id PASSED
