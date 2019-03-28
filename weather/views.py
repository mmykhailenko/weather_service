from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import requests
from weather_service_api import config
from rest_framework.views import APIView
from .models import Weather, Forecast
from .serializer import UserSerializer, GroupSerializer, WeatherSerializer, ForecastSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class WeatherDetail(APIView):

    def get(self, request, city):

        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(city, config.API_KEY)

        if request.method == 'GET':
            resp = requests.get(url).json()

            res = {
                "city_name": resp.get("name"),
                "cord_lon": resp["coord"]["lon"],
                "cord_lat": resp["coord"]["lat"],
                "weather_main": resp["weather"][0]["main"],
                "weather_description": resp["weather"][0]["description"],
                "date_time": resp.get("dt"),
                "temp": resp["main"]["temp"]
            }
        serializer = WeatherSerializer(data=res)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WeatherList(APIView):

    def get(self, request, format=None):
        weather = Weather.objects.all()
        serializer = WeatherSerializer(weather, many=True)
        return Response(serializer.data)


class ForecastList(APIView):

    def get(self, request, format=None):
        forecast = Forecast.objects.all()
        serializer = ForecastSerializer(forecast, many=True)
        return Response(serializer.data)


class ForecastDetail(APIView):

    def get(self, request, city, cnt):

        forecast_url = "http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&cnt={}&appid={}".\
            format(city, cnt, config.API_KEY)

        if request.method == "GET":
            resp = requests.get(forecast_url).json()
            results = []
            res2 = {}
            res1 = {'city_name': resp["city"]["name"],
                    'cord_lon': resp["city"]["coord"]["lon"],
                    'cord_lat': resp["city"]["coord"]["lat"]
                    }
            for i in resp['list']:
                res2['date_time'] = i['dt_txt']
                res2['temp'] = i['main']['temp']
                res2['weather_description'] = i['weather'][0]['description']
                res2['weather_main'] = i['weather'][0]['main']
                result = {**res1, **res2}
                serializer = ForecastSerializer(data=result)

                if serializer.is_valid():
                    serializer.save()
                    results.append(result)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer2 = ForecastSerializer(data=results, many=True)
            if serializer2.is_valid():
                return Response(serializer2.data, status=status.HTTP_201_CREATED)



