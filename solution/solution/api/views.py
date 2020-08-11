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
