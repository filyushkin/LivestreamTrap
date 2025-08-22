# Запуск проекта

## 1) Docker Desktop terminal

`docker run -d --name redis -p 6379:6379 redis`

(опционально: `docker run --name redis -p 6379:6379 redis`)

## 2) PyCharm terminal 1

`celery -A LivestreamTrap worker -l info --pool=solo`

(опционально: `celery -A LivestreamTrap worker -l info --pool=threads`)

## 3) PyCharm terminal 2

`celery -A LivestreamTrap beat -l info`

## 4) PyCharm terminal 3

`python manage.py runserver`
