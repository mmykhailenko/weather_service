from rest_framework import serializers
from weather.models.city_model import City


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('city_name', 'cord_lon', 'cord_lat')
