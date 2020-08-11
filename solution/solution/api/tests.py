import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from solution.api.models import Car, Tyre
from solution.api.serializers import CarSerializer, TyreSerializer


client = Client()

class CreateCar(TestCase):
    """ Test car creation """
    def setup(self):
        [Car.objects.create() for _ in range(3)]

    def test_list_cars(self):
        response = client.get(reverse('endpoint_function_name_here'))
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
