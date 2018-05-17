from sim.phisics import *
from sim.world import *

@static_vars(counter=0)
class Partition(object):
    def __init__(self, u, size, rooms=[]):
        self.u = u
        self.counter = Partition.counter
        Partition.counter += 1

        # Size in meters squared
        self.size = size

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
        movingHeat = self.u * self.size * temperatureDifference * delta

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
        self.__setTemperature = 0
        self.light = 0
        self.__setLight = 0

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self.__setTemperature = value

    def addHeat(self, energy):
        # Recalculate temperature
        world = World()
        self._temperature += energy / (MaterialDensity['air'](self.temperature, world.pressure) * self.volume * SpecificHeats['air'])

class OutsideRoom(Room):
    def __init__(self, name):
        Room.__init__(self, name, 1)

    @property
    def temperature(self):
        # TODO(mkarol) Get outside temperature on given moment of simulation
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        pass

    def addHeat(self, energy):
        pass

class GroundRoom(Room):
    def __init__(self, name):
        Room.__init__(self, name, 1)

    @property
    def temperature(self):
        # TODO(mkarol) Get ground temperature on given moment of simulation
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

    roomsInitMap = {
        '0-Area1': {
            'volume': 421.23,
        },
        '0-Area2': {
            'volume': 16.87,
        },
        '0-Area3': {
            'volume': 59.26,
        },
        '0-Area4': {
            'volume': 39.80,
        },
        '0-Area5': {
            'volume': 20.252,
        },
        '1-Area1': {
            'volume': 65.79,
        },
        '1-Area2': {
            'volume': 83.04,
        },
        '1-Area3': {
            'volume': 42.00,
        },
        '1-Area4': {
            'volume': 38.43,
        },
        '1-Area5': {
            'volume': 63.07,
        },
    }
    roomsObjectMap = {}
    rooms = []

    outside = OutsideRoom('Outside')
    roomsObjectMap['Outside'] = outside
    rooms.append(outside)

    ground = GroundRoom('Ground')
    roomsObjectMap['Ground'] = ground
    rooms.append(ground)

    for key in roomsInitMap:
        room = Room(key, roomsInitMap[key]['volume'])
        roomsObjectMap[key] = room

        rooms.append(room)

    building.rooms = rooms

    roomsObjectMap['0-Area1'].addHeat(1000000)
    print(roomsObjectMap['0-Area1'].temperature)

    # 0-Area1
    Partition(u=0.122, size=50.53, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['Outside']])
    Partition(u=0.122, size=21.60, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['Outside']])
    Partition(u=0.124, size=32.00, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['Outside']])
    Partition(u=0.124, size=22.11, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['Outside']])

    Partition(u=1.637, size=9.45, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['0-Area5']])
    Partition(u=1.981, size=3.57, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['0-Area3']])
    Partition(u=1.981, size=11.68, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['0-Area4']])
    Partition(u=1.981, size=8.63, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['0-Area5']])
    Partition(u=1.981, size=7.02, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['0-Area2']])
    Partition(u=1.981, size=6.31, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['0-Area3']])

    Partition(u=1.637, size=14.62, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['1-Area3']])
    Partition(u=10, size=6.83, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['1-Area3']])
    Partition(u=1.637, size=7.78, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['1-Area3']])

    Partition(u=0.171, size=71.84, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['Ground']])
    Partition(u=0.133, size=32.00, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['Outside']])
    Partition(u=0.297, size=7.41, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['1-Area1']])
    Partition(u=0.297, size=10.78, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['1-Area2']])
    Partition(u=0.297, size=10.15, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['1-Area3']])
    Partition(u=0.297, size=3.52, rooms=[roomsObjectMap['0-Area1'], roomsObjectMap['1-Area5']])

    # 0-Area2
    Partition(u=1.981, size=8.723, rooms=[roomsObjectMap['0-Area2'], roomsObjectMap['0-Area5']])
    Partition(u=1.981, size=8.723, rooms=[roomsObjectMap['0-Area2'], roomsObjectMap['0-Area3']])

    Partition(u=0.122, size=6.405, rooms=[roomsObjectMap['0-Area2'], roomsObjectMap['Outside']])
    Partition(u=0.171, size=5.530, rooms=[roomsObjectMap['0-Area2'], roomsObjectMap['Ground']])
    Partition(u=0.297, size=4.06, rooms=[roomsObjectMap['0-Area2'], roomsObjectMap['1-Area4']])
    Partition(u=0.297, size=1.80, rooms=[roomsObjectMap['0-Area2'], roomsObjectMap['1-Area5']])

    # 0-Area3
    Partition(u=0.122, size=16.775, rooms=[roomsObjectMap['0-Area3'], roomsObjectMap['Outside']])
    Partition(u=0.122, size=12.200, rooms=[roomsObjectMap['0-Area3'], roomsObjectMap['Outside']])

    Partition(u=1.981, size=10.37, rooms=[roomsObjectMap['0-Area3'], roomsObjectMap['0-Area4']])

    Partition(u=0.171, size=19.43, rooms=[roomsObjectMap['0-Area3'], roomsObjectMap['Ground']])
    Partition(u=0.297, size=19.43, rooms=[roomsObjectMap['0-Area3'], roomsObjectMap['1-Area5']])

    # 0-Area4
    Partition(u=0.122, size=10.37, rooms=[roomsObjectMap['0-Area4'], roomsObjectMap['Outside']])
    Partition(u=0.122, size=11.59, rooms=[roomsObjectMap['0-Area4'], roomsObjectMap['Outside']])

    Partition(u=0.171, size=39.8025, rooms=[roomsObjectMap['0-Area4'], roomsObjectMap['Ground']])
    Partition(u=0.297, size=39.8025, rooms=[roomsObjectMap['0-Area4'], roomsObjectMap['1-Area1']])

    # 0-Area5
    Partition(u=0.122, size=7.869, rooms=[roomsObjectMap['0-Area5'], roomsObjectMap['Outside']])

    Partition(u=0.171, size=6.64, rooms=[roomsObjectMap['0-Area5'], roomsObjectMap['Ground']])
    Partition(u=0.297, size=6.64, rooms=[roomsObjectMap['0-Area5'], roomsObjectMap['1-Area4']])

    # Level I
    # 1-Area1
    Partition(u=0.122, size=14.62, rooms=[roomsObjectMap['1-Area1'], roomsObjectMap['Outside']])
    Partition(u=0.122, size=20.61, rooms=[roomsObjectMap['1-Area1'], roomsObjectMap['Outside']])

    Partition(u=1.981, size=11.39, rooms=[roomsObjectMap['1-Area1'], roomsObjectMap['1-Area2']])
    Partition(u=1.981, size=3.23, rooms=[roomsObjectMap['1-Area1'], roomsObjectMap['1-Area3']])
    Partition(u=1.981, size=15.30, rooms=[roomsObjectMap['1-Area1'], roomsObjectMap['1-Area5']])

    Partition(u=0.133, size=17.33, rooms=[roomsObjectMap['1-Area1'], roomsObjectMap['Outside']])

    # 1-Area2
    Partition(u=0.122, size=26.01, rooms=[roomsObjectMap['1-Area2'], roomsObjectMap['Outside']])

    Partition(u=1.981, size=21.30, rooms=[roomsObjectMap['1-Area2'], roomsObjectMap['1-Area3']])

    Partition(u=0.133, size=14.68, rooms=[roomsObjectMap['1-Area2'], roomsObjectMap['Outside']])

    # 1-Area3
    Partition(u=1.981, size=3.60, rooms=[roomsObjectMap['1-Area3'], roomsObjectMap['1-Area5']])
    Partition(u=1.981, size=7.83, rooms=[roomsObjectMap['1-Area3'], roomsObjectMap['1-Area5']])
    Partition(u=1.981, size=12.57, rooms=[roomsObjectMap['1-Area3'], roomsObjectMap['1-Area4']])

    Partition(u=0.133, size=12.24, rooms=[roomsObjectMap['1-Area3'], roomsObjectMap['Outside']])

    # 1-Area4
    Partition(u=0.122, size=8.81, rooms=[roomsObjectMap['1-Area4'], roomsObjectMap['Outside']])

    Partition(u=1.981, size=7.78, rooms=[roomsObjectMap['1-Area4'], roomsObjectMap['1-Area5']])

    Partition(u=0.133, size=12.59, rooms=[roomsObjectMap['1-Area4'], roomsObjectMap['Outside']])

    # 1-Area5
    Partition(u=0.122, size=11.25, rooms=[roomsObjectMap['1-Area5'], roomsObjectMap['Outside']])
    Partition(u=0.122, size=20.54, rooms=[roomsObjectMap['1-Area5'], roomsObjectMap['Outside']])

    Partition(u=0.133, size=25.96, rooms=[roomsObjectMap['1-Area5'], roomsObjectMap['Outside']])

    return building
