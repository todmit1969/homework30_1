Проект представляет собой Django-приложение с использованием Docker Compose. Включает следующие сервисы (с названиями на уровне docker-compose):

web — backend (выполняет миграции и запускает сервер: python manage.py migrate --settings=config.settings_docker && python manage.py runserver 0.0.0.0:8000 --settings=config.settings_docker).
db — PostgreSQL (версия 15).
redis — Redis (версия 7, используется как брокер/кеш).
celery — Celery worker.
celery-beat — Celery Beat (планировщик задач).