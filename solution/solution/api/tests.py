import math
import solution.api.constants as constants
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from solution.api.models import Car, Tyre
from solution.api.serializers import CarSerializer, TyreSerializer
from solution.api.helpers import degradate_tyres, find_older_tyre


client = Client()

# TODO: add base_url
class LongTripTest(TestCase):
    """ Test 10.000 KM trip """

    def setUp(self):
        self.car = Car.objects.create(gas=100)
        self.url = f'http://localhost:8000/api/v1/cars/{self.car.id}/trip/'
        self.data = { 'distance': 10000 }
        self.tyres = [Tyre.objects.create(car_id=self.car.id) for _ in range(4)]
        self.car_final_state = {
            'id': self.car.id,
            'gas': 0,
            'gas_capacity': self.car.gas_capacity,
            'tyres': self.tyres
        }


    def test_ten_thousand_km_trip(self):
        distance_to_refuel = self.refuel_distance(self.car.gas)
        distance_to_replace_tyre = self.replace_tyre_distance(self.tyres)

        self.travel(distance_to_refuel, distance_to_replace_tyre)


    def travel(self, distance_to_refuel, distance_to_replace_tyre):
        distance = self.data['distance']
        while distance:
            if distance_to_refuel == 0:
                distance_to_refuel = self.stop_to_refuel()
            if distance_to_replace_tyre < constants.TYRE_MIN_ENDURANCE_DISTANCE:
                distance_to_replace_tyre = self.stop_to_replace_tyre()

            min_distance = min(distance_to_refuel, distance_to_replace_tyre)

            response = client.post(self.url, data={ 'distance': min_distance }, content_type='application/json', format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            distance = 0 if min_distance > distance else distance - min_distance
            if distance == 0:
                break

            distance_to_refuel -= min_distance
            distance_to_replace_tyre -= min_distance
            trip_degradation = min_distance * constants.TYRE_DEGRADATION_PER_KM
            degradate_tyres(self.tyres, trip_degradation)


    def stop_to_refuel(self):
        url = f'http://localhost:8000/api/v1/cars/{self.car.id}/refuel/'
        data = { 'gas': self.car.gas_capacity }
        client.put(url, data=data, content_type='application/json')
        car = Car.objects.get(id=self.car.id)
        return self.refuel_distance(car.gas)


    def stop_to_replace_tyre(self):
        url = f'http://localhost:8000/api/v1/cars/{self.car.id}/maintenance/'
        tyres = Tyre.objects.filter(car_id=self.car.id)
        older_tyre = find_older_tyre(tyres)
        data = { 'tyre_id': older_tyre.__dict__['id'] }
        client.put(url, data=data, content_type='application/json')
        return self.replace_tyre_distance(tyres)


    def get_car_state(self):
        url = f'http://localhost:8000/api/v1/cars/{self.car.id}'
        response = client.get(url, content_type='application/json', format='json')
        self.car = response.data
        self.tyres = response.data['tyres']


    def refuel_distance(self, gas):
        print(f'=> current gas {gas}')
        return gas * self.car.gas_capacity * constants.KM_PER_LITER / constants.PERCENTAGE


    def replace_tyre_distance(self, tyres):
        older_tyre = find_older_tyre(tyres)
        older_tyre_endurance = constants.TYRE_MAX_ENDURANCE - older_tyre.degradation
        return older_tyre_endurance * constants.TYRE_DISTANCE_ENDURANCE
