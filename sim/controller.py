from sim.world import *
from sim.physics import *

class Controller(object):
    def __init__(self, building):
        self.building = building


    def step(self, state, delta):
        world = World()
        localBuilding = state.building

        for i in range(0, len(localBuilding.rooms)):
            room = localBuilding.rooms[i]
            energyError = (room.setTemperature - room.temperature) * (MaterialDensity['air'](celciusDegreeToKelvin(room.temperature), world.pressure) * room.volume * SpecificHeats['air'])
            room.addHeat(room.hvac.controller.getPower(energyError, delta))

        state.building = localBuilding
