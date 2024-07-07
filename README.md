# SimetraTest

Работа с alembic - 
1. alembic init migrations
2. migrations.env.py добавляем строчки
   - config.set_main_option('sqlalchemy.url', f"{settings.DATABASE_URL}?async_fallback=True")
   - sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
   - from src.models import VehicleData
3. Создаем таблицы - alembic revision --autogenerate -m "ini"
4. Апдейтим до последней версии - alembic upgrade head

Собираем образ - docker build -t test_task .
Запускаем контейнер - docker run -d -p 5473:80 test_task
Запускаем парсер в src/pars

Подключаемся к эндпоинтам по адресу - http://0.0.0.0:5473/docs