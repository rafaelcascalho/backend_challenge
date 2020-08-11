def degradate_tyres(tyres, trip_degradation):
    for tyre in tyres:
        tyre.degradation += trip_degradation
        tyre.save()


def find_older_tyre(tyres):
    return min(tyres, key=lambda tyre: tyre.degradation)
