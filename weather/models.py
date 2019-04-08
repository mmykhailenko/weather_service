from django.db import models

# Create your models here.


class Weather(models.Model):
    city_name = models.TextField(max_length=100)
    cord_lon = models.TextField()
    cord_lat = models.TextField()
    weather_main = models.TextField()
    weather_description = models.TextField()
    temp = models.TextField()
    date_time = models.TextField()
