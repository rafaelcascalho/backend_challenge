from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from .models import Car, Tyre
from rest_framework import status
from rest_framework import viewsets
from .serializers import CarSerializer, TyreSerializer
from .services import CarService
from .errors import EXCEPTIONS


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all().order_by('created_at')
    serializer_class = CarSerializer
    car_service = CarService()


    @action(methods=['put'], detail=True, url_path='refuel')
    def refuel(self, request, *args, **kwargs):
        try:
            id, gas = kwargs['pk'], request.data['gas']
            car = Car.objects.get(id=id)
            gas = self.car_service.refuel(car, gas)
            return Response(data={ 'gas': gas }, status=status.HTTP_200_OK)
        except Exception as exception:
            exception_name = exception.args[0]
            if exception_name not in EXCEPTIONS:
                exception_name = 'default'
            exception = EXCEPTIONS[exception_name]
            return Response(data=exception['data'], status=exception['status'])



    @action(methods=['post'], detail=True, url_path='tyres/create')
    def create_tyre(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            if not Car.objects.get(id=id):
                raise Exception('NotFound')
            tyre = self.car_service.create_tyre(id)
            serializer = TyreSerializer(tyre)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exception:
            exception_name = exception.args[0]
            if exception_name not in EXCEPTIONS:
                exception_name = 'default'
            exception = EXCEPTIONS[exception_name]
            return Response(data=exception['data'], status=exception['status'])



    @action(methods=['put'], detail=True, url_path='maintenance')
    def replace(self, request, *args, **kwargs):
        try:
            car_id, tyre_id = kwargs['pk'], request.data['tyre_id']
            if not Car.objects.get(id=car_id):
                raise Exception('NotFound')
            car = self.car_service.replace(car_id, tyre_id)
            serializer = CarSerializer(car)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            exception_name = exception.args[0]
            if exception_name not in EXCEPTIONS:
                exception_name = 'default'
            exception = EXCEPTIONS[exception_name]
            return Response(data=exception['data'], status=exception['status'])



    @action(methods=['post'], detail=True, url_path='trip')
    def trip(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            distance = request.data['distance']
            if not Car.objects.get(id=id):
                raise Exception('NotFound')
            car = self.car_service.trip(id, distance)
            serializer = CarSerializer(car)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            exception_name = exception.args[0]
            if exception_name not in EXCEPTIONS:
                exception_name = 'default'
            exception = EXCEPTIONS[exception_name]
            return Response(data=exception['data'], status=exception['status'])


