from rest_framework.response import Response
from rest_framework import status
from weather_service_api import config
import requests
from rest_framework.views import APIView
from weather.serializers.forecast_serializer import ForecastSerializer
from weather.config import FORECAST_CITY_DAYS_URL


class ForecastDetail(APIView):

    """
       3h weather forecast in the city
          """

    def get(self, request, city, cnt):

        forecast_url = FORECAST_CITY_DAYS_URL.format(city, cnt, config.API_KEY)

        response = requests.get(forecast_url).json()
        if response.get('cod') == '404':
            return Response(response, status=400)
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









