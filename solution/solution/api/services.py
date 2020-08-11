from solution.api.models import Car, Tyre
import solution.api.constants as constants
import math


class CarService():
    def refuel(self, car, gas):
        if car.gas > constants.LOW_GAS:
            raise Exception('NoNeedForRefuel')

        new_quantity = car.gas + gas
        if new_quantity > car.gas_capacity:
            raise Exception('GasOverflow')
        
        car.gas = new_quantity
        car.save()
        return new_quantity


    def replace(self, car_id, tyre_id):
        tyres = Tyre.objects.filter(car_id=car_id)
        search = [tyre for tyre in tyres if tyre.id == tyre_id]
        if search == []:
            raise Exception('TyreNotFoundInCar')

        old_tyre = search[0]
        if not old_tyre.degradation > constants.MIN_DEGRATATION:
            raise Exception('NoNeedForReplacement')

        old_tyre.delete()
        tyre = Tyre.objects.create(car_id=car_id)
        return Car.objects.get(id=car_id)


    def create_tyre(self, car_id):
        tyres = Tyre.objects.filter(car_id=car_id)
        degradated = [tyre for tyre in tyres if tyre.degradation > constants.MIN_DEGRATATION]
        tyres_number = len(tyres)
        if tyres_number - len(degradated) == constants.MAX_TYRES:
            raise Exception('MaxTyres')            

        tyre = Tyre.objects.create(car_id=car_id)
        return tyre


    def trip(self, car_id, distance):
        car = Car.objects.get(id=car_id)
        required_gas = distance / constants.KM_PER_LITER
        if required_gas > car.gas:
            raise Exception('NotEnoughGas')

        tyres = Tyre.objects.filter(car_id=car_id)
        older_tyre = min(tyres, key=lambda tyre: tyre.degradation)
        older_tyre_endurance = constants.TYRE_MAX_ENDURANCE - older_tyre.degradation
        trip_degradation = distance * constants.TYRE_DEGRADATION_PER_KM
        if older_tyre_endurance < trip_degradation:
            raise Exception('TyreTore')

        self.degradate_tyres(tyres, trip_degradation)
        car.gas -= required_gas
        car.save()
        return car


    def degradate_tyres(self, tyres, trip_degradation):
        for tyre in tyres:
            tyre.degradation += trip_degradation
            tyre.save()