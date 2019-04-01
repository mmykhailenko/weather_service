from django.contrib.auth.models import User, Group
from rest_framework import serializers


from .models import Weather, Forecast, City


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('city_name', 'cord_lon', 'cord_lat')


class WeatherSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Weather
        fields = ('city', 'weather_main', 'weather_description', 'temp', 'date_time')

    def create(self, validated_data):
        city_data = validated_data.pop("city")
        city, _ = City.objects.get_or_create(city_name=city_data['city_name'],
                                             cord_lon=city_data['cord_lon'],
                                             cord_lat=city_data['cord_lat'],)
        weather, created = Weather.objects.get_or_create(city=city,
                                                         date_time=validated_data['date_time'],
                                                         defaults={
                                                            'weather_main': validated_data['weather_main'],
                                                            'weather_description': validated_data['weather_description'],
                                                            'temp': validated_data['temp']})
        return weather


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
                                                            'weather_description': validated_data['weather_description'],
                                                            'temp': validated_data['temp']})

        return weather
