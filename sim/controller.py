class Controller(object):
    def __init__(self, building):
        self.building = building


    def step(self, state, delta):
        # TODO (mkarol) create controllers for each room PID

        localBuilding = state.building
        state.building = localBuilding
