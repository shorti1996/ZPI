class Simulation(object):

    def __init__(self, state):
        self.state = state

    def step(self, delta):
        localBuilding = self.state.building

        # Temperature calcuations
        partitions = set()
        for room in localBuilding.rooms:
            partitions.update(room.partitions)

        for partition in partitions:
            partition.recalculateTemperatures(delta)

        for i in range(0, len(localBuilding.rooms)):
            localBuilding.rooms[i].light = localBuilding.rooms[i].light + 2

        self.state.building = localBuilding


