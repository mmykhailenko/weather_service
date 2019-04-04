from django.db import models

# Create your models here.
from .city_model import City


class Forecast(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    weather_main = models.TextField()
    weather_description = models.TextField()
    temp = models.CharField(max_length=100, default='temp')
    date_time = models.TextField()

    class Meta:
        unique_together = ('city', 'date_time')





