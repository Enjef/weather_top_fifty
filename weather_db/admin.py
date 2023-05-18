from django.contrib import admin
from weather_db.models import City, Weather

admin.site.register(City)
admin.site.register(Weather)
