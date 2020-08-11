from django.db import models
from random import randint


class Car(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    gas_capacity = models.FloatField(default=100)
    gas = models.FloatField(default=100)


class Tyre(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    degradation = models.FloatField(default=0)
    car = models.ForeignKey(Car, related_name='tyres', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.degradation)
