from rest_framework.response import Response
import requests
from rest_framework.views import APIView
from weather.models.forecast_model import Forecast
from weather.serializers.forecast_serializer import ForecastSerializer


class ForecastList(APIView):

    """
    List of all requests for 3h weather forecasts
       """

    def get(self, request):
        forecast = Forecast.objects.all()
        serializer = ForecastSerializer(forecast, many=True)
        return Response(serializer.data)


