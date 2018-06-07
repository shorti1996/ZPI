from sim.world import *
from sim.physics import *

class Controller(object):
    def __init__(self, state, lock):
        self.state = state
        self.lock = lock


    def step(self, state, delta):
        world = World()
        self.lock.acquire()
        localBuilding = self.state.building

        for i in range(0, len(localBuilding.rooms)):
            room = localBuilding.rooms[i]
            energyError = (room.setTemperature - room.temperature) * (MaterialDensity['air'](celciusDegreeToKelvin(room.temperature), world.pressure) * room.volume * SpecificHeats['air'])
            power = room.hvac.controller.getPower(energyError, delta)
            room.hvac.power = abs(power)
            room.addHeat(power)

        self.state.building = localBuilding
        self.lock.release()
