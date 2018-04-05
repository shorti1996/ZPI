from sim.world import *
from sim.home import *
from sim.simulation import *
from sim.controller import *
from multiprocessing import Process, Manager
import time

def createSimulation(state, delta=0.01):
    simulation = Simulation(state)
    controller = Controller(state)

    # Way of keeping constatnt FPS
    FPS = 10
    start = time.time()
    simulation.step(delta)
    controller.step(state, delta)
    end = time.time()
    sleepInterval = (1 / FPS) - (start - end)

    while True:
        simulation.step(delta)
        controller.step(state, delta)
        print("Simulation Works")
        time.sleep(sleepInterval)

def startController(delta=0.01):
    world = World()
    building = generateBuilding()

    # Create state
    manager = Manager()
    state = manager.Namespace()
    state.building = building
    world.state = state

    process = Process(target=createSimulation, args=[world.state, delta])
    process.start()




