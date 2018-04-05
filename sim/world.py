from sim.simulation import *
from sim.controller import *
from sim.home import *
from multiprocessing import Process
import csv
import time


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class World(object, metaclass=Singleton):
    state = None

def createSimulation(state, delta=0.01):
    simulation = Simulation(state.building)
    controller = Controller(state.building)

    # Way of keeping constatnt FPS
    FPS = 10
    start = time.time()
    simulation.step(state, delta)
    controller.step(state, delta)
    end = time.time()
    sleepInterval = (1 / FPS) - (start - end)

    while True:
        simulation.step(state, delta)
        controller.step(state, delta)
        print("Simulation Works")
        time.sleep(sleepInterval)

def startController(delta=0.01):
    world = World()
    building = generateBuilding()
    world.state = createBuildingState(building)
    process = Process(target=createSimulation, args=[world.state, delta])
    process.start()










def get_weather_hourly():
    with open('sim/weather_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            data.append(row)
            yield row
        # for row in data:
        #     print(row['STATION'], row['DATE'])


def yielder(arg):
    z = 0
    for x in arg:
        z = z + 1
        print("z= " + str(z))
        yield 2 * x

gen = get_weather_hourly()
print(gen)
print(gen.__next__()["NAME"])

# x = 10
# for i in get_weather_hourly():
#     if x > 0:
#         print(i["DATE"])
#         x = x - 1




