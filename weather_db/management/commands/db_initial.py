from weather_db.models import City
from django.core.management.base import BaseCommand
import csv


class Command(BaseCommand):
    help = 'Заполняем базу 50 крупнейшими по населению городами'

    def handle(self, *args, **kwargs):
        all_cities = dict()
        with open('initial_data/cities_list.csv', 'r') as csvfile:
            all_cities_list = csv.reader(csvfile)
            for city_name, lon, lat, _ in all_cities_list:
                all_cities[city_name] = (lon, lat)

        with open('initial_data/top_cities.csv', 'r') as csvfile:
            top_cities_list = csv.reader(csvfile)
            for (city_name,) in top_cities_list:
                lon, lat = all_cities[city_name]
                City.objects.get_or_create(
                    title=city_name,
                    latitude=float(lat),
                    longitude=float(lon)
                )
            print('db_initial is Done')
        return
