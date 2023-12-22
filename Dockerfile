## Базовый образ для сборки
FROM python:3.10-slim

# Указываем рабочую директорию
WORKDIR /usr/src/app

# Запрещаем Python писать файлы .pyc на диск
ENV PYTHONDONTWRITEBYTECODE 1
# Запрещает Python буферизовать stdout и stderr
ENV PYTHONUNBUFFERED 1

# Установка зависимостей проекта
COPY ./pyproject.toml ./poetry.lock ./alembic.ini ./entrypoint.sh ./

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        python3-dev \
        libpq-dev \
    # install packages
    && python -m pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root \
    # clean
    && rm -rf /root/.cache \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq autoremove \
    && apt-get clean

# Копируем проект
COPY ./src ./src
