from rest_framework.response import Response
from rest_framework import status
from weather_service_api import config
import requests
from rest_framework.views import APIView
from weather.serializers.weather_serializer import WeatherSerializer
from weather.config import WEATHER_LON_LAT_URL

CURR_LOCATION_URL = "https://api.ipdata.co?api-key=test"


class WeatherCurrentLocation(APIView):
    """
    get:
    Get weather in city, found by current ip address
    """

    @staticmethod
    def get_current_location():
        r = requests.get(CURR_LOCATION_URL).json()
        lat = r['latitude']
        lon = r['longitude']
        return {'lat': lat, 'lon': lon}

    def get_weather_by_location(self):
        location = self.get_current_location()
        return requests.get(WEATHER_LON_LAT_URL.format(location['lat'], location['lon'], config.API_KEY))

    def get(self, request):
        response = self.get_weather_by_location().json()
        if response["cod"] != 200:
            return Response(response["message"], status=status.HTTP_400_BAD_REQUEST)

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
