from rest_framework import status
from rest_framework.response import Response

EXCEPTIONS = {
    'NotFound': {
        'data': { 'error': 'car not found' },
        'status': status.HTTP_404_NOT_FOUND
    },
    'MaxTyres': {
        'data': { 'error': 'car already have 4 tyres in good state' },
        'status': status.HTTP_400_BAD_REQUEST
    },
    'TyreTore': {
        'data': { 'error': 'a tyre tore' },
        'status': status.HTTP_422_UNPROCESSABLE_ENTITY
    },
    'NotEnoughGas': {
        'data': { 'error': 'not enough gas' },
        'status': status.HTTP_422_UNPROCESSABLE_ENTITY
    },
    'TyreNotFoundInCar': {
        'data': { 'error': 'tyre not found in car' },
        'status': status.HTTP_404_NOT_FOUND
    },
    'NoNeedForReplacement': {
        'data': { 'error': 'tyre is still in good state' },
        'status': status.HTTP_422_UNPROCESSABLE_ENTITY
    },
    'NoNeedForRefuel': {
        'data': { 'error': 'car has more than 5% gas' },
        'status': status.HTTP_422_UNPROCESSABLE_ENTITY
    },
    'GasOverflow': {
        'data': { 'error': 'too much gas for the tank' },
        'status': status.HTTP_422_UNPROCESSABLE_ENTITY
    },
    'default': {
        'data': { 'error': 'server internal error' },
        'status': status.HTTP_500_INTERNAL_SERVER_ERROR
    }
}
