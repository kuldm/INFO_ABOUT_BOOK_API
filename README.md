# Проект: API для управления информацией о книгах, авторах и тегах

## Описание

Этот проект представляет собой API для управления информацией о книгах, авторах и тегах. API поддерживает операции CRUD (создание, получение, обновление, удаление) для книг, авторов и тегов, а также авторизацию пользователей по токену. Проект разработан с использованием FastAPI, PostgreSQL, SQLAlchemy и Pydantic.

### Основные возможности:

- Регистрация и авторизация пользователей
- Авторизация пользователей с помощью токенов
- CRUD операции для книг, авторов и тегов
- Возможность фильтрации книг по авторам и тегам
- Документация API через Swagger

## Стек технологий

- Backend: FastAPI (Python 3.11)
- База данных: PostgreSQL
- Асинхронные операции: asyncio, SQLAlchemy
- ORM: SQLAlchemy, Pydantic
- Контейнеризация: Docker Compose

## Установка и запуск проекта

Для запуска проекта вам необходимо иметь установленный Docker и Docker Compose. Следуйте инструкциям ниже для развертывания приложения.

### 1. Клонирование репозитория

Клонируйте репозиторий с исходным кодом проекта на вашу локальную машину:

```
git clone https://github.com/kuldm/INFO_ABOUT_BOOK_API.git
```

Перейдите в папку с проектом:

```
cd INFO_ABOUT_BOOK_API 
```

### 2. Настройка переменных окружения
Создайте файл `.env` и `.env-non-dev` в корне проекта и **добавьте необходимые переменные окружения** для подключения к базе данных PostgreSQL:

Для `.env`:
```
echo 
MODE=DEV
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_user
DB_PASS=your_password
DB_NAME=info_about_book_api
TEST_DB_HOST=localhost
TEST_DB_PORT=5432
TEST_DB_USER=your_user
TEST_DB_PASS=your_password
TEST_DB_NAME=test_info_about_book_api
SECRET_KEY=pYVbNH23969EfjVrg69d++GgdZmCoc6aKaxFIQf3rh8=
ALGORITHM=HS256
HOST=0.0.0.0
PORT=8000 > .env
```

Для `.env-non-dev`:


```
echo 
MODE=DEV
DB_HOST=db
DB_PORT=5432
DB_USER=your_user
DB_PASS=your_password
DB_NAME=info_about_book_api
POSTGRES_USER=info_about_book_api
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
SECRET_KEY=pYVbNH23969EfjVrg69d++GgdZmCoc6aKaxFIQf3rh8=
ALGORITHM=HS256
HOST=0.0.0.0
PORT=8000 > .env-non-dev
```

### 3. Сборка и запуск контейнеров
Для сборки и запуска всех контейнеров выполните следующие команды:

```docker compose build```
и
```docker compose up```


### 4. Проверка работы API

После успешного запуска контейнеров, API будет доступен по адресу: 
`http://localhost:7777`

Документация Swagger будет доступна по адресу:
`http://localhost:7777/docs`

### 5. Остановка контейнеров

Чтобы остановить и удалить контейнеры, выполните команду:

```docker compose down```

## API эндпоинты
### Авторизация
- POST /auth/register — Регистрация нового пользователя
- POST /auth/login — Авторизация пользователя и получение JWT токена
- POST /auth/logout — Разлогинивание пользователя
- DELETE /auth/{username} — Удаление пользователя
### Книги (Books)
- GET /books — Получение списка всех книг
- POST /books — Создание новой книги
- GET /books/{id} — Получение книги по ID
- PUT /books/{id} — Обновление информации о книге
- DELETE /books/{id} — Удаление книги
### Авторы (Authors)
- GET /authors — Получение списка всех авторов
- POST /authors — Создание нового автора
- GET /authors/{id} — Получение автора по ID
- PUT /authors/{id} — Обновление информации об авторе
- DELETE /authors/{id} — Удаление автора
### Теги (Tags)
- GET /tags — Получение списка всех тегов
- POST /tags — Создание нового тега
- GET /tags/{id} — Получение тега по ID
- PUT /tags/{id} — Обновление информации о теге
- DELETE /tags/{id} — Удаление тега

\
**Этот файл README.md предоставляет полную инструкцию по настройке, сборке и запуску вашего проекта с использованием Docker. Он также содержит описание основных функций API и команды для работы с контейнерами.**