class Controller(object):
    def __init__(self, building):
        self.building = building


    def step(self, state, delta):
        # TODO (mkarol) create controllers for each room PID

        localBuilding = state.building

        # TODO (mkarol) simulate single step
        for i in range(0, len(state.building.rooms)):
            localBuilding.rooms[i].light = localBuilding.rooms[i].light - 1

        state.building = localBuilding
