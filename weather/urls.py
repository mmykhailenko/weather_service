from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from weather.views import weather_detail_view, forecast_detail_view, weather_list_view, forecast_list_view, \
    weather_current_location_view

urlpatterns = [

    path('weather/current', weather_current_location_view.WeatherCurrentLocation().as_view()),
    path('weather/<str:city>', weather_detail_view.WeatherDetail.as_view()),
    path('forecast/<str:city>/<int:cnt>', forecast_detail_view.ForecastDetail.as_view()),
    path('weather/', weather_list_view.WeatherList.as_view()),
    path('forecast/', forecast_list_view.ForecastList.as_view())
]


git staurlpatterns = format_suffix_patterns(urlpatterns)
