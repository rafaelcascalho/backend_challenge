from solution.api.models import Car, Tyre
import solution.api.constants as constants

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

    # TODO:test
    def replace(self, car, new_tyre):
        replacable = [tyre for tyre in car.tyres if tyre.degradation > constants.MAX_TYRES_IN_USE]
        if replacable == []:
            raise Exception('NoNeedForMaintenance')
        replacable[0].delete()
        car.tyres.append(new_tyre)
        return car

    def create_tyre(self, car_id):
        tyres = Tyre.objects.filter(car_id=car_id)
        if len(tyres) == 4:
            raise Exception('MaxTyres')
        tyre = Tyre.objects.create(car_id=car_id)
        return tyre

    # TODO: test
    def trip(self):
        pass
