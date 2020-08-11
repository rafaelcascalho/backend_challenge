from .models import Car, Tyre
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer


class TyreSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Tyre
        fields = ['id', 'degradation']


class CarSerializer(FlexFieldsModelSerializer):
    tyres = TyreSerializer(many=True, required=False)


    class Meta:
        model = Car
        fields = ['id', 'gas_capacity', 'gas', 'tyres']
        expandable_fields = { 'tyres': (TyreSerializer, { 'many': True }) }
