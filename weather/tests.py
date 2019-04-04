from django.test import TestCase
from weather.models.city_model import City
from weather.serializers.city_serializer import CitySerializer


class CitySaveTestCase(TestCase):
    def setUp(self):
        data = {
            "city_name": "Odessa", 
            "cord_lon": "30.72", 
            "cord_lat": "46.48"
        }

        serializer = CitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()

    def test_city_save(self):
        """
            City that is saved in database can be retrieved
        """

        odessa = City.objects.get(city_name="Odessa")
        
        self.assertEqual(odessa.city_name, "Odessa")
        self.assertEqual(odessa.cord_lon, "30.72")
        self.assertEqual(odessa.cord_lat, "46.48")

