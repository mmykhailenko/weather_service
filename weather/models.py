from django.db import models

# Create your models here.


class City(models.Model):
    city_name = models.CharField(max_length=100, default='city_name')
    cord_lon = models.CharField(max_length=100, default='cord_lon')
    cord_lat = models.CharField(max_length=100, default='cord_lat')


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    weather_main = models.TextField()
    weather_description = models.TextField()
    temp = models.CharField(max_length=100, default='temp')
    date_time = models.TextField()

    class Meta:
        unique_together = ('city', 'date_time')


class Forecast(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    weather_main = models.TextField()
    weather_description = models.TextField()
    temp = models.CharField(max_length=100, default='temp')
    date_time = models.TextField()

    class Meta:
        unique_together = ('city', 'date_time')




