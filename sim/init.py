from sim.world import *
from sim.building import *
from sim.simulation import *
from sim.controller import *
from multiprocessing import Process, Manager
from sim.world_utils import *
from sim.models import TemperatureHistory, LightHistory

import time


def createSimulation(state):
    simulation = Simulation(state)
    controller = Controller(state)

    animatingFunction = addPlotingBuilding(state)

    # Way of keeping constant FPS
    FPS = 1
    delta = 1 / FPS
    start = time.time()
    simulation.step(delta)
    controller.step(state, delta)
    animatingFunction()
    end = time.time()
    sleepInterval = (1 / FPS) - (start - end)
    counter = 1

    while 1:
        counter = counter + 1

        # Every FPS add second to timestamp
        if counter % FPS == 0:
            state.timestamp = state.timestamp + 1

        # Every 60 simulation second add history
        if counter % (60 * FPS) == 0:
            for room in state.building.rooms:
                TemperatureHistory.objects.create(timestamp=state.timestamp, room_id=room.id, value=room.temperature)
                for light in room.lights.values():
                    LightHistory.objects \
                        .create(timestamp=state.timestamp, room_id=room.id, light_id=light.id, value=light.state)

            TemperatureHistory.objects.create(timestamp=state.timestamp, room_id=state.building.outside.id,
                                              value=state.building.outside.temperature)

            animatingFunction()

        # Every 3600 simulation second clear history and clear counter
        if counter % (3600 * FPS) == 0:
            TemperatureHistory.objects.filter(timestamp__lt=state.timestamp - 100).delete()
            LightHistory.objects.filter(timestamp__lt=state.timestamp - 100).delete()
            counter = 0

        simulation.step(delta)
        controller.step(state, delta)

        # time.sleep(sleepInterval)


def startController():
    world = World()
    building = generateBuilding()

    # Create state
    manager = Manager()
    state = manager.Namespace()
    state.building = building
    # 01.01.2017
    state.timestamp = 1483228800
    world.state = state

    # Clear history
    TemperatureHistory.objects.all().delete()
    LightHistory.objects.all().delete()

    # Create simulation
    process = Process(target=createSimulation, args=[world.state])
    process.start()




