from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from weather import views

urlpatterns = [

    path('weather/current', views.WeatherCurrentLocation().as_view()),
    path('weather/<str:city>', views.WeatherDetail.as_view()),
    path('forecast/<str:city>/<int:cnt>', views.ForecastDetail.as_view()),
    path('weather/', views.WeatherList.as_view()),
    path('forecast/', views.ForecastList.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
