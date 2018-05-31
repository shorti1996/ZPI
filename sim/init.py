from sim.world import *
from sim.building import *
from sim.simulation import *
from sim.controller import *
from multiprocessing import Process, Manager, Lock
from sim.world_utils import *
from sim.models import TemperatureHistory, LightHistory, PowerHistory

import time


def createSimulation(state):
    simulation = Simulation(state)
    controller = Controller(state)

    # animatingFunction = addPlotingBuilding()

    # Way of keeping constant FPS
    FPS = 1
    delta = 1 / FPS
    # start = time.time()
    # simulation.step(delta)
    # controller.step(state, delta)
    # animatingFunction()
    # end = time.time()
    # sleepInterval = (1 / FPS) - (start - end)
    counter = 1

    while 1:
        counter = counter + 1

        simulation.step(delta)
        controller.step(state, delta)

        localBuilding = state.building
        # Power calcuations
        for room in localBuilding.rooms:
            room.hvac.summedPower = room.hvac.summedPower + room.hvac.power
            for light in room.lights.values():
                light.summedPower = light.summedPower + light.power/delta
        state.building = localBuilding

        # Every FPS add second to timestamp
        if counter % FPS == 0:
            state.timestamp = state.timestamp + 1

        # Every 60 simulation second add history
        if counter % (60 * FPS) == 0:
            for room in state.building.rooms:
                TemperatureHistory.objects.create(timestamp=state.timestamp, room_id=room.id, value=room.temperature)
                PowerHistory.objects.create(timestamp=state.timestamp, room_id=room.id,
                                            lightValue=sum(map(lambda light: light.summedPower, room.lights.values()))/60, climatValue=room.hvac.summedPower/60)
                for light in room.lights.values():
                    LightHistory.objects \
                        .create(timestamp=state.timestamp, room_id=room.id, light_id=light.id, value=light.state)

            TemperatureHistory.objects.create(timestamp=state.timestamp, room_id=state.building.outside.id,
                                              value=state.building.outside.temperature)

            # Clearing history
            # TemperatureHistory.objects.filter(timestamp__lte=state.timestamp - 1800).delete()
            # LightHistory.objects.filter(timestamp__lte=state.timestamp - 1800).delete()
            # PowerHistory.objects.filter(timestamp__lte=state.timestamp - 1800).delete()

            # animatingFunction()

            # Power calcuations
            for room in state.building.rooms:
                room.hvac.summedPower = 0
                for light in room.lights.values():
                    light.summedPower = 0

        # Every 3600 simulation second clear counter
        if counter % (3600 * FPS) == 0:
            counter = 0

        time.sleep(0.001)


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
    PowerHistory.objects.all().delete()

    # Create simulation
    process = Process(target=createSimulation, args=[world.state])
    process.start()




