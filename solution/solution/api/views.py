from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from .models import Car, Tyre
from rest_framework import status
from rest_framework import viewsets
from .serializers import CarSerializer, TyreSerializer
from .services import CarService


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
            return Response(data={ 'gas': gas }, status=status.HTTP_201_CREATED)
        except Exception as exception:
            print(exception)
            if exception.args[0] == 'NoNeedForRefuel':
                return Response(data={ 'error': 'car has more than 5% gas' }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            elif exception.args[0] == 'GasOverflow':
                return Response(data={ 'error': 'too much gas for the tank' }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return Response(data={ 'error' : 'Server Internal Error' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            print(exception)
            if exception.args[0] == 'MaxTyres':
                return Response(data={ 'error': 'car already have 4 tyres in good state' }, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={ 'error' : 'Server Internal Error' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
