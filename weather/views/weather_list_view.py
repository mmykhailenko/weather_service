from rest_framework.response import Response
import requests
from rest_framework.views import APIView
from weather.models.weather_model import Weather
from weather.serializers.weather_serializer import WeatherSerializer


class WeatherList(APIView):

    """
        List of all requests for current weather
           """

    def get(self, request):
        weather = Weather.objects.all()
        serializer = WeatherSerializer(weather, many=True)
        return Response(serializer.data)
