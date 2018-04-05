from sim.home import *

class Simulation(object):

    def __init__(self, building):
        self.building = building

    def step(self, state, delta):
        localBuilding = state.building

        # TODO (mkarol) simulate single step
        for i in range(0, len(state.building.rooms)):
            localBuilding.rooms[i].light = localBuilding.rooms[i].light + 2

        state.building = localBuilding
