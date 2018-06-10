from sim.physics import *
from sim.world import *
@static_vars(id=0)
class PID(object):
    def __init__(self, init_object, min_power, max_power):
        self.p = init_object['p']
        self.i = init_object['i']
        self.d = init_object['d']
        self.min_power = min_power
        self.max_power = max_power
        self.summ = 0
        self.lerror = None
        self.id = PID.id
        PID.id = PID.id + 1

    def getPower(self, error, delta):
        if self.lerror is None:
            self.lerror = error
        self.summ = self.summ + error * delta
        out = (self.p * error) + (self.p * self.i * self.summ) + (self.p * self.d * (error - self.lerror) / delta)
        self.lerror = error
        return max(min(out, self.max_power), self.min_power)


@static_vars(id=0)
class Light(object):
    def __init__(self, friendly_name, power):
        self.name = friendly_name
        self.state = False
        self.id = Light.id
        self._power = power
        self.summedPower = 0
        Light.id = Light.id + 1

    @property
    def power(self):
        return self._power if self.state else 0

@static_vars(id=0)
class HVAC(object):
    def __init__(self, heating_power, cooling_power, controller):
        self.id = HVAC.id
        HVAC.id = HVAC.id + 1
        self.heating_power = heating_power
        self.cooling_power = cooling_power
        self.controller = PID(controller, -cooling_power, heating_power)
        self.summedPower = 0

@static_vars(id=0)
class Partition(object):
    def __init__(self, u, size, rooms=[]):
        self.u = u
        self.id = Partition.id
        Partition.id = Partition.id + 1

        # Size in meters squared
        self.size = size

        self.rooms = rooms
        for room in rooms:
            room.partitions.append(self)

    def recalculateTemperatures(self, delta):
        if len(self.rooms) == 0 or len(self.rooms) > 2:
            return

        temperatureDifference = self.rooms[0].temperature - self.rooms[1].temperature
        movingHeat = self.u * self.size * temperatureDifference * delta

        self.rooms[0].addHeat(-movingHeat)
        self.rooms[1].addHeat(movingHeat)

    def __cmp__(self, other):
        return self.id - other.id

@static_vars(id=0)
class Room(object):
    dummyInit = {
        'volume': 0,
        'lights': [],
        'hvac': {
            'heating_power': 0,
            'cooling_power': 0,
            'controller': {
                'p': 0,
                'i': 0,
                'd': 0,
            },
        },
    }

    def __init__(self, name, init_object=dummyInit):
        self.id = Room.id
        Room.id = Room.id + 1
        self.name = name
        self.volume = init_object['volume']
        self.sensors = []
        self.utilities = []
        self.partitions = []
        self._temperature = 20
        self._setTemperature = 24
        self.lights = {obj.id: obj for obj in list(map(lambda light_data: Light(light_data['name'], light_data['power']), init_object['lights']))}
        self.hvac = HVAC(init_object['hvac']['heating_power'], init_object['hvac']['cooling_power'], init_object['hvac']['controller'])

    @property
    def temperature(self):
        return self._temperature

    @property
    def setTemperature(self):
        return self._setTemperature

    @temperature.setter
    def temperature(self, value):
        self._setTemperature = value

    @property
    def light(self):
        return self._light

    @light.setter
    def light(self, value):
        self._light = value

    def addHeat(self, energy):
        # Recalculate temperature
        world = World()
        self._temperature += energy / (MaterialDensity['air'](physics.celciusDegreeToKelvin(self.temperature),
                                                              world.pressure) * self.volume * SpecificHeats['air'])


class OutsideRoom(Room):
    def __init__(self, name):
        Room.__init__(self, name)
        self._temperature = 0
        self._setTemperature = 0
        self.isSystem = True

    @property
    def temperature(self):
        world = World()
        return world.weather.get_weather(world.state.timestamp)[Weather.TEMP]

    @temperature.setter
    def temperature(self, value):
        pass

    def addHeat(self, energy):
        pass


class GroundRoom(Room):
    def __init__(self, name):
        Room.__init__(self, name)
        self._temperature = 0
        self._setTemperature = 0
        self.isSystem = True

    @property
    def temperature(self):
        world = World()
        return world.soil.get_soil(world.state.timestamp)[Soil.TEMP]

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

    roomsInitMap = {
        'Kuchnia, salon, korytarz': {
            'volume': 421.23,
            'lights': [
                            {
                                'name': 'Glowne oswietlenie',
                                'power': 60,
                            },
                            {
                                'name': 'Glowne oswietlenie',
                                'power': 60,
                            },
                            {
                                'name': 'Lampka na biurku',
                                'power': 20,
                            },
                            {
                                'name': 'Kinkiet',
                                'power': 40,
                            },
                        ],
            'hvac': {
                'heating_power': 3200,
                'cooling_power': 2500,
                'controller': {
                    'p': 1,
                    'i': 0,
                    'd': 0,
                },
            },
        },
        'Lazienka': {
            'volume': 16.87,
            'lights': [],
            'hvac': {
                'heating_power': 3200,
                'cooling_power': 2500,
                'controller': {
                    'p': 1,
                    'i': 0,
                    'd': 0,
                },
            },
        },
        'Gabinet': {
            'volume': 59.26,
            'lights': [],
            'hvac': {
                'heating_power': 3200,
                'cooling_power': 2500,
                'controller': {
                    'p': 1,
                    'i': 0,
                    'd': 0,
                },
            },
        },
        'Wiatrolap, garderoba': {
            'volume': 39.80,
            'lights': [],
            'hvac': {
                'heating_power': 3200,
                'cooling_power': 2500,
                'controller': {
                    'p': 1,
                    'i': 0,
                    'd': 0,
                },
            },
        },
        'Pom. gospodarcze': {
            'volume': 20.252,
            'lights': [],
            'hvac': {
                'heating_power': 3200,
                'cooling_power': 2500,
                'controller': {
                    'p': 1,
                    'i': 0,
                    'd': 0,
                },
            },
        },
        'Pokoj dziecka 1': {
            'volume': 65.79,
            'lights': [],
            'hvac': {
                'heating_power': 3200,
                'cooling_power': 2500,
                'controller': {
                    'p': 1,
                    'i': 0,
                    'd': 0,
                },
            },
        },
        'Pokoj dziecka 2': {
            'volume': 83.04,
            'lights': [],
            'hvac': {
                'heating_power': 3200,
                'cooling_power': 2500,
                'controller': {
                    'p': 1,
                    'i': 0,
                    'd': 0,
                },
            },
        },
        'Korytarz': {
            'volume': 42.00,
            'lights': [],
            'hvac': {
                'heating_power': 3200,
                'cooling_power': 2500,
                'controller': {
                    'p': 1,
                    'i': 0,
                    'd': 0,
                },
            },
        },
        'Lazienka, pralnia': {
            'volume': 38.43,
            'lights': [],
            'hvac': {
                'heating_power': 3200,
                'cooling_power': 2500,
                'controller': {
                    'p': 1,
                    'i': 0,
                    'd': 0,
                },
            },
        },
        'Sypialnia, garderoba': {
            'volume': 63.07,
            'lights': [],
            'hvac': {
                'heating_power': 3200,
                'cooling_power': 2500,
                'controller': {
                    'p': 1,
                    'i': 0,
                    'd': 0,
                },
            },
        },
    }
    roomsObjectMap = {}
    rooms = []

    for key, description in roomsInitMap.items():
        room = Room(key, description)
        roomsObjectMap[key] = room
        rooms.append(room)

    building.rooms = rooms

    outside = OutsideRoom('Outside')
    roomsObjectMap['Outside'] = outside
    building.outside = outside

    ground = GroundRoom('Ground')
    roomsObjectMap['Ground'] = ground
    building.ground = ground

    # Kuchnia, salon, korytarz
    Partition(u=0.122, size=50.53, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Outside']])
    Partition(u=0.122, size=21.60, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Outside']])
    Partition(u=0.124, size=32.00, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Outside']])
    Partition(u=0.124, size=22.11, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Outside']])

    Partition(u=1.637, size=9.45, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Pom. gospodarcze']])
    Partition(u=1.981, size=3.57, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Gabinet']])
    Partition(u=1.981, size=11.68, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Wiatrolap, garderoba']])
    Partition(u=1.981, size=8.63, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Pom. gospodarcze']])
    Partition(u=1.981, size=7.02, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Lazienka']])
    Partition(u=1.981, size=6.31, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Gabinet']])

    Partition(u=1.637, size=14.62, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Korytarz']])
    Partition(u=10, size=6.83, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Korytarz']])
    Partition(u=1.637, size=7.78, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Korytarz']])

    Partition(u=0.171, size=71.84, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Ground']])
    Partition(u=0.133, size=32.00, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Outside']])
    Partition(u=0.297, size=7.41, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Pokoj dziecka 1']])
    Partition(u=0.297, size=10.78, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Pokoj dziecka 2']])
    Partition(u=0.297, size=10.15, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Korytarz']])
    Partition(u=0.297, size=3.52, rooms=[roomsObjectMap['Kuchnia, salon, korytarz'], roomsObjectMap['Sypialnia, garderoba']])

    # Lazienka
    Partition(u=1.981, size=8.723, rooms=[roomsObjectMap['Lazienka'], roomsObjectMap['Pom. gospodarcze']])
    Partition(u=1.981, size=8.723, rooms=[roomsObjectMap['Lazienka'], roomsObjectMap['Gabinet']])

    Partition(u=0.122, size=6.405, rooms=[roomsObjectMap['Lazienka'], roomsObjectMap['Outside']])
    Partition(u=0.171, size=5.530, rooms=[roomsObjectMap['Lazienka'], roomsObjectMap['Ground']])
    Partition(u=0.297, size=4.06, rooms=[roomsObjectMap['Lazienka'], roomsObjectMap['Lazienka, pralnia']])
    Partition(u=0.297, size=1.80, rooms=[roomsObjectMap['Lazienka'], roomsObjectMap['Sypialnia, garderoba']])

    # Gabinet
    Partition(u=0.122, size=16.775, rooms=[roomsObjectMap['Gabinet'], roomsObjectMap['Outside']])
    Partition(u=0.122, size=12.200, rooms=[roomsObjectMap['Gabinet'], roomsObjectMap['Outside']])

    Partition(u=1.981, size=10.37, rooms=[roomsObjectMap['Gabinet'], roomsObjectMap['Wiatrolap, garderoba']])

    Partition(u=0.171, size=19.43, rooms=[roomsObjectMap['Gabinet'], roomsObjectMap['Ground']])
    Partition(u=0.297, size=19.43, rooms=[roomsObjectMap['Gabinet'], roomsObjectMap['Sypialnia, garderoba']])

    # Wiatrolap, garderoba
    Partition(u=0.122, size=10.37, rooms=[roomsObjectMap['Wiatrolap, garderoba'], roomsObjectMap['Outside']])
    Partition(u=0.122, size=11.59, rooms=[roomsObjectMap['Wiatrolap, garderoba'], roomsObjectMap['Outside']])

    Partition(u=0.171, size=39.8025, rooms=[roomsObjectMap['Wiatrolap, garderoba'], roomsObjectMap['Ground']])
    Partition(u=0.297, size=39.8025, rooms=[roomsObjectMap['Wiatrolap, garderoba'], roomsObjectMap['Pokoj dziecka 1']])

    # Pom. gospodarcze
    Partition(u=0.122, size=7.869, rooms=[roomsObjectMap['Pom. gospodarcze'], roomsObjectMap['Outside']])

    Partition(u=0.171, size=6.64, rooms=[roomsObjectMap['Pom. gospodarcze'], roomsObjectMap['Ground']])
    Partition(u=0.297, size=6.64, rooms=[roomsObjectMap['Pom. gospodarcze'], roomsObjectMap['Lazienka, pralnia']])

    # Level I
    # Pokoj dziecka 1
    Partition(u=0.122, size=14.62, rooms=[roomsObjectMap['Pokoj dziecka 1'], roomsObjectMap['Outside']])
    Partition(u=0.122, size=20.61, rooms=[roomsObjectMap['Pokoj dziecka 1'], roomsObjectMap['Outside']])

    Partition(u=1.981, size=11.39, rooms=[roomsObjectMap['Pokoj dziecka 1'], roomsObjectMap['Pokoj dziecka 2']])
    Partition(u=1.981, size=3.23, rooms=[roomsObjectMap['Pokoj dziecka 1'], roomsObjectMap['Korytarz']])
    Partition(u=1.981, size=15.30, rooms=[roomsObjectMap['Pokoj dziecka 1'], roomsObjectMap['Sypialnia, garderoba']])

    Partition(u=0.133, size=17.33, rooms=[roomsObjectMap['Pokoj dziecka 1'], roomsObjectMap['Outside']])

    # Pokoj dziecka 2
    Partition(u=0.122, size=26.01, rooms=[roomsObjectMap['Pokoj dziecka 2'], roomsObjectMap['Outside']])

    Partition(u=1.981, size=21.30, rooms=[roomsObjectMap['Pokoj dziecka 2'], roomsObjectMap['Korytarz']])

    Partition(u=0.133, size=14.68, rooms=[roomsObjectMap['Pokoj dziecka 2'], roomsObjectMap['Outside']])

    # Korytarz
    Partition(u=1.981, size=3.60, rooms=[roomsObjectMap['Korytarz'], roomsObjectMap['Sypialnia, garderoba']])
    Partition(u=1.981, size=7.83, rooms=[roomsObjectMap['Korytarz'], roomsObjectMap['Sypialnia, garderoba']])
    Partition(u=1.981, size=12.57, rooms=[roomsObjectMap['Korytarz'], roomsObjectMap['Lazienka, pralnia']])

    Partition(u=0.133, size=12.24, rooms=[roomsObjectMap['Korytarz'], roomsObjectMap['Outside']])

    # Lazienka, pralnia
    Partition(u=0.122, size=8.81, rooms=[roomsObjectMap['Lazienka, pralnia'], roomsObjectMap['Outside']])

    Partition(u=1.981, size=7.78, rooms=[roomsObjectMap['Lazienka, pralnia'], roomsObjectMap['Sypialnia, garderoba']])

    Partition(u=0.133, size=12.59, rooms=[roomsObjectMap['Lazienka, pralnia'], roomsObjectMap['Outside']])

    # Sypialnia, garderoba
    Partition(u=0.122, size=11.25, rooms=[roomsObjectMap['Sypialnia, garderoba'], roomsObjectMap['Outside']])
    Partition(u=0.122, size=20.54, rooms=[roomsObjectMap['Sypialnia, garderoba'], roomsObjectMap['Outside']])

    Partition(u=0.133, size=25.96, rooms=[roomsObjectMap['Sypialnia, garderoba'], roomsObjectMap['Outside']])

    return building
