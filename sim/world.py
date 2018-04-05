import csv

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@static_vars(pressure=100000)
class World(object, metaclass=Singleton):
    state = None


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




