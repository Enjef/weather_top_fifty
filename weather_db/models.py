from django.db import models


class City(models.Model):
    title = models.TextField(verbose_name='Latin',)
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self) -> str:
        return f'{self.title}'


class Weather(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name='Город',
    )
    cur_temp = models.FloatField(verbose_name='Температура',)
    humidity = models.IntegerField(verbose_name='Влажность',)
    pressure = models.IntegerField(verbose_name='Давление',)
    weather_description = models.TextField(verbose_name='Состояние',)
    wind_speed = models.FloatField(verbose_name='Ветер',)
    date = models.DateTimeField(verbose_name='Время',)
    timezone_shift = models.IntegerField(verbose_name='Смещение таймзоны',)

    class Meta:
        ordering = ('date',)
        verbose_name = 'Погода'
        verbose_name_plural = 'Погода'

    def __str__(self) -> str:
        return f'Погода в {self.city.title}'
