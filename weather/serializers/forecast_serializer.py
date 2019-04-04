from rest_framework import serializers
from weather.models.city_model import City
from weather.models.forecast_model import Forecast
from .city_serializer import CitySerializer


class ForecastSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Forecast
        fields = ('city', 'weather_main', 'weather_description', 'temp', 'date_time')

    def create(self, validated_data):
        city_data = validated_data.pop("city")
        city, _ = City.objects.get_or_create(city_name=city_data['city_name'],
                                             cord_lon=city_data['cord_lon'],
                                             cord_lat=city_data['cord_lat'],)

        weather, created = Forecast.objects.get_or_create(city=city,
                                                          date_time=validated_data['date_time'],
                                                          defaults={
                                                              'weather_main': validated_data['weather_main'],
                                                              'weather_description':
                                                                  validated_data['weather_description'],
                                                              'temp': validated_data['temp']})

        return weather
