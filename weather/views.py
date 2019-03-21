from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests

from weather.models import Weather
from weather.serializer import UserSerializer, GroupSerializer, WeatherSerializer


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


@api_view(['GET'])
def weather_save(request, city):
    API_KEY = "6034d87efaa342b60bd74f470f24eb86"
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city, API_KEY)

    if request.method == 'GET':
        resp = requests.get(url).json()

        res = {
            "city_name": resp.get("name"),
            "cord_lon": resp["coord"]["lon"],
            "cord_lat": resp["coord"]["lat"],
            "weather_main": resp["weather"][0]["main"],
            "weather_description": resp["weather"][0]["main"],
            "date_time": resp.get("dt"),
            "temp": resp["main"]["temp"]
        }

        serializer = WeatherSerializer(data=res)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def weather_get(request):
    if request.method == 'GET':
        weather = Weather.objects.all()
        serializer = WeatherSerializer(weather, many=True)
        return Response(serializer.data)
