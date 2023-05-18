# Проект: weather_top_fifty
Приложение собирает данные о погоде в 50 крупнейших городах мира,
на основании этих данных будет происходить управление охлаждением
и нагрузкой Дата-центров.

### Описание
Приложение реализованно на Django, запрос на api https://openweathermap.org/
осуществляется раз в час с помощью экземпляра класса Collector.
Collector при создании экземпляра использует API-KEY и функцию parser, это
позволяет использовать его с разными видами API.

Openweathermap предоставляет разнообразные погодные и астрономические данные,
которые могут быть использованы в дальнейшем для решения возникающих задач.
Для этого нужно создать новую модель Weather с необходимыми полями,
написать парсер для этой модели и использовать новый парсер в коллекторе.

Сейчас база городов формируется из списка 50 крупнейших по населению городов
по данным википедии.
По этому списку подтягиваются координаты из списка 372 крупнейших городов (файл
с сайта openweathermap).
В дальнейшем можно дополнить модель City различными показателями и периодически
их обновлять. При изменении критерия вхождения в топ, необходимо отсортировать
города по нужному полю и, сформировав актуальный список, отправить его в
функцию collect коллектора.

### Технологии
Использовал последние версии
- Python 3.9.13
- django 4.2.1
- docker-compose 3.8
- postgres:12.4

Ключи и пароли не скрыты для демонстрации работы коллектора в упрощенном формате.
Раздачу статики организовал через WhiteNoise.

### Запуск проекта

Выполните команды:
```
docker-compose up -d
docker-compose exec web python manage.py makemigrations weather_db
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py db_initial
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py runcollector
```

### Optional

Выполните команды для запуска сервера:
```
docker-compose exec web python manage.py runserver 0.0.0.0:8000
```
Так можно через админку убедиться что данные сохраняются в необходимом
виде http://localhost:8000/admin.

Или напрямую запросом к базе в образе.
```
docker-compose exec -it db psql -U postgres -c 'SELECT * FROM weather_db_weather;'
```
