class TransportStrategy:
    async def calculate(self, distance, weight):
        raise NotImplementedError()

    def eta(self):
        raise NotImplementedError()


class MiniVanStrategy(TransportStrategy):
    async def calculate(self, distance, weight):
        return distance * weight * 3

    def eta(self):
        return 2


class TruckStrategy(TransportStrategy):
    async def calculate(self, distance, weight):
        return distance * weight * 2

    def eta(self):
        return 4


class AirplaneStrategy(TransportStrategy):
    async def calculate(self, distance, weight):
        return distance * weight * 1

    def eta(self):
        return 1


def transport_factory(distance, delivery_speed):

    if delivery_speed == "express" and distance > 300:
        return AirplaneStrategy(), "Aeroplane"

    if distance <= 100:
        return MiniVanStrategy(), "Mini Van"
    elif distance <= 500:
        return TruckStrategy(), "Truck"
    else:
        return AirplaneStrategy(), "Aeroplane"
