from multiprocessing import Manager

class Partition(object):
    def __init__(self, lam, size, rooms=[]):
        self.lam = lam

        # Size in meters squared
        self.size = size

        self.rooms = rooms
        for room in rooms:
            room.partitions.append(self)

    def recalculateTemperatures(self):
        if len(self.rooms) == 0 or len(self.rooms) > 2:
            return

        colderRoom = 0 if self.rooms[0].temperature < self.rooms[1].temperature else 1



class Room(object):
    def __init__(self, name):
        self.name = name
        self.sensors = []
        self.utilities = []
        self.partitions = []
        self.temperature = 0
        self.__setTemperature = 0
        self.light = 0
        self.__setLight = 0

    def setTemperature(self, y):
        self.__setTemperature = y + 253



class Building(object):
    def __init__(self):
        self.rooms = []

# Generating
def generateBuilding():
    building = Building()

    namesOfRooms = ['Outside', 'RoomA', 'RoomB', 'RoomC', 'RoomD']
    rooms = []
    for name in namesOfRooms:
        room = Room(name)
        rooms.append(room)
        building.rooms.append(room)

    Partition(0.01, 100, [rooms[1], rooms[2]])
    Partition(0.01, 50, [rooms[2], rooms[3]])

    return building

def createBuildingState(building):
    manager = Manager()
    state = manager.Namespace()
    state.building = building
    return state