from django.db import models

# Create your models here.


class City(models.Model):
    city_name = models.CharField(max_length=100, default='city_name')
    cord_lon = models.CharField(max_length=100, default='cord_lon')
    cord_lat = models.CharField(max_length=100, default='cord_lat')

