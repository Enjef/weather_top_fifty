import logging
import os
import threading
from datetime import datetime, timezone
from time import sleep

import requests
from django.core.management.base import BaseCommand

from weather_db.models import City, Weather

logging.basicConfig(
    filename='weather_db_logs/weather_collector.log',
    level=logging.ERROR,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


def current_weather_parser(city, api_key):
    lat, lon = city.latitude, city.longitude
    data = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
    ).json()
    wind = float(data.get('wind', {'speed': 0})['speed'])
    Weather.objects.create(
        city=city,
        cur_temp=data['main']['temp'],
        humidity=data['main']['humidity'],
        pressure=data['main']['pressure'],
        weather_description=data['weather'][0]['main'],
        wind_speed=wind,
        date=datetime.fromtimestamp(data['dt'], tz=timezone.utc),
        timezone_shift=data['timezone'],
    )
    return


class Collector:
    def __init__(self, api_key, parser) -> None:
        self.api_key = api_key
        self.parser = parser

    def collect(self, cities):
        while True:
            start = datetime.now()
            for city in cities:
                try:
                    self.parser(city, self.api_key)
                except KeyboardInterrupt:
                    break
                except Exception as ex:
                    print(ex)
                    logging.exception(f'Не удалось сохранить данные для {city.title}: {ex}')
            print('Collection done in', datetime.now()-start)
            sleep(3600)


class Command(BaseCommand):
    help = 'Получаем данные о 50 крупнейших городах мира и сохраняем в базу'

    def handle(self, *args, **kwargs):
        api_key = os.environ.get('OPENWEATHER_API_KEY')
        top_cities = City.objects.all()
        weather_collector = Collector(api_key, current_weather_parser)
        collector_thread = threading.Thread(
            target=weather_collector.collect, args=(top_cities,))
        collector_thread.start()
