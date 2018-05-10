from sim.phisics import *
from sim.world import *


@static_vars(counter=0)
class Partition(object):
    def __init__(self, lam, size, thickness, rooms=[]):
        self.lam = lam
        self.counter = Partition.counter
        Partition.counter += 1

        # Size in meters squared
        self.size = size

        # Thickness in meters
        self.thickness = thickness

        self.rooms = rooms
        for room in rooms:
            room.partitions.append(self)

    def recalculateTemperatures(self, delta):
        if len(self.rooms) == 0 or len(self.rooms) > 2:
            return

        # Heat goes from hotter room [0] to colder [1]
        if self.rooms[0].temperature < self.rooms[1].temperature:
            # Swap
            self.rooms[0], self.rooms[1] = self.rooms[1], self.rooms[0]

        temperatureDifference = self.rooms[0].temperature - self.rooms[1].temperature
        movingHeat = (self.lam * self.size * temperatureDifference * delta) / self.thickness

        self.rooms[0].addHeat(-movingHeat)
        self.rooms[1].addHeat(movingHeat)

    def __cmp__(self, other):
        return self.counter - other.counter


class Room(object):
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume
        self.sensors = []
        self.utilities = []
        self.partitions = []
        self._temperature = 0
        self._setTemperature = 0
        self.light = False

    @property
    def temperature(self):
        return self._temperature

    @property
    def setTemperature(self):
        return self._setTemperature

    @temperature.setter
    def temperature(self, value):
        self._setTemperature = value

    def addHeat(self, energy):
        # Recalculate temperature
        world = World()
        self._temperature += energy / (MaterialDensity['air'](self.temperature, world.pressure) * self.volume * SpecificHeats['air'])


class OutsideRoom(Room):
    def __init__(self, name):
        Room.__init__(self, name, 1)

    @property
    def temperature(self):
        # TODO(mkarol) Get temperature on given moment of simulation
        return self._temperature

    @property
    def setTemperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        pass

    def addHeat(self, energy):
        pass


class Building(object):
    def __init__(self):
        self.rooms = []


# Generating
def generateBuilding():
    # Building
    building = Building()

    namesOfRoomsAndVolumes = [('RoomA', 10)]
    rooms = []

    outside = OutsideRoom("Outside")

    building.rooms.append(outside)
    rooms.append(outside)

    for name, volume in namesOfRoomsAndVolumes:
        room = Room(name, volume)
        rooms.append(room)
        building.rooms.append(room)

    rooms[1].addHeat(1000000)
    print(rooms[1].temperature)

    Partition(lam=MaterialHeatConductivity['reinforced concrete'], size=100, thickness=0.1, rooms=[rooms[0], rooms[1]])

    return building
