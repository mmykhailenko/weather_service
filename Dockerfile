FROM python:3

RUN mkdir -p /opt/weather_service
WORKDIR /opt/weather_service

COPY . /opt/weather_service/

RUN pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:$PORT
