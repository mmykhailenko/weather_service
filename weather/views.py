from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.views import APIView

from weather.consts import NOT_FOUND_RESP_CODE
from .models import Weather, Forecast, City
from .serializer import UserSerializer, GroupSerializer, WeatherSerializer, ForecastSerializer, CitySerializer
from weather.config import WEATHER_CITY_URL, FORECAST_CIRY_DAYS_URL, WEATHER_LON_LAT_URL

CURR_LOCATION_URL = "https://api.ipdata.co?api-key=test"

API_KEY = "6034d87efaa342b60bd74f470f24eb86"


class UserViewSet(viewsets.ModelViewSet):
    """
    get:
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    get:
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class WeatherDetail(APIView):
    """
    get:
    Return current weather in teh specified city
    """

    def get(self, request, city):
        url = WEATHER_CITY_URL.format(city, config.API_KEY)

        response = requests.get(url).json()

        if NOT_FOUND_RESP_CODE in response.get('cod'):
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


class WeatherList(APIView):

    def get(self, request):
        weather = Weather.objects.all()
        serializer = WeatherSerializer(weather, many=True)
        return Response(serializer.data)


class ForecastList(APIView):

    def get(self, request):
        forecast = Forecast.objects.all()
        serializer = ForecastSerializer(forecast, many=True)
        return Response(serializer.data)


class ForecastDetail(APIView):

    def get(self, request, city, cnt):

        forecast_url = FORECAST_CIRY_DAYS_URL.format(city, cnt, config.API_KEY)
        response = requests.get(forecast_url).json()

        if NOT_FOUND_RESP_CODE in response.get('cod'):
            return Response(response, status=404)

        weather_data = []
        res1 = {"city": {
            'city_name': response["city"]["name"],
            'cord_lon': response["city"]["coord"]["lon"],
            'cord_lat': response["city"]["coord"]["lat"]}
        }
        res2 = {}
        for i in response['list']:
            res2['weather_main'] = i['weather'][0]['main']
            res2['weather_description'] = i['weather'][0]['description']
            res2['temp'] = i['main']['temp']
            res2['date_time'] = i['dt']
            result = {**res1, **res2}
            weather_data.append(result)
        serializer = ForecastSerializer(data=weather_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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



