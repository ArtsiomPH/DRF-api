Проект упакован в докер контейнер.

## Запуск проекта

```sh
docker compose build
docker compose up -d
```

## Создание суперпользователя

Логин: admin<br>
Пароль: admin

```sh
docker compose run --rm api make create_admin
```

## Запуск тестов

```sh
docker compose run --rm api make test
```

## Запуск линтеров

```sh
docker compose run --rm api make lint
```

## Форматирование

```sh
docker compose run --rm api make format_code
```