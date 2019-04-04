from rest_framework.response import Response
from rest_framework import status
from weather_service_api import config
import requests
from rest_framework.views import APIView
from weather.serializers.weather_serializer import WeatherSerializer
from weather.config import WEATHER_CITY_URL


class WeatherDetail(APIView):

    """
        Сurrent weather in the city
           """

    def get(self, request, city):
        url = WEATHER_CITY_URL.format(city, config.API_KEY)

        response = requests.get(url).json()
        if response.get('cod') != 200:
            return Response(response, status=400)
        data = {
            "city": {
                "city_name": response.get("name"),
                "cord_lon": response["coord"]["lon"],
                "cord_lat": response["coord"]["lat"]
            },
            "weather_main": response["weather"][0]["main"],
            "weather_description": response["weather"][0]["description"],
            "temp": response["main"]["temp"],
            "date_time": response.get("dt")
        }

        serializer = WeatherSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
