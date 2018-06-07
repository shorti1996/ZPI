class Simulation(object):

    def __init__(self, state, lock):
        self.state = state
        self.lock = lock

    def step(self, delta):
        self.lock.acquire()
        localBuilding = self.state.building
        # Temperature calcuations
        partitions = set()
        for room in localBuilding.rooms:
            partitions.update(room.partitions)

        for partition in partitions:
            partition.recalculateTemperatures(delta)

        self.state.building = localBuilding
        self.lock.release()


