import csv
import time
from dateutil import parser
from sim import world_utils

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
    # def __init__(self, curr_timestamp):
    #     self.weather = WeatherCsv('weather_data.csv')
    #     if curr_timestamp == 0:
            # pass
        # else:
        #     self.timestamp = curr_timestamp

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


class Weather:
    """
    Static keys for returning similar dicts for different implementations
    """
    TEMP = "temp"

    # @abc.abstractmethod
    def get_weather(self, timestamp):
        raise NotImplementedError("You must implement __get_weather__")


class WeatherCsv(Weather):
    DATE_FMT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, filename):
        self.weather_data = self.load_weather_data(filename)

    @staticmethod
    def load_weather_data(filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = []
            for row in reader:
                data.append(row)
            return data

    def get_weather(self, timestamp):
        if timestamp == 0:
            return {Weather.TEMP: self.weather_data[0]["HLY-TEMP-NORMAL"]}
        else:
            for x in self.weather_data:
                date = datetime.datetime.strptime("2010-" + x["DATE"], WeatherCsv.DATE_FMT)
                if date.timestamp() > timestamp:
                    return self.weather_from_row(x)

    @staticmethod
    def weather_from_row(row):
        result = dict()
        result[Weather.TEMP] = WeatherCsv.fahrenheit_to_celcius(float(row["HLY-TEMP-NORMAL"]))
        return result

    @staticmethod
    def fahrenheit_to_celcius(fahrenheit):
        return (fahrenheit - 32) / 1.8

if __name__ == '__main__':
    world = World(0)
    print(world.weather.get_weather(0)[Weather.TEMP])

    time_test = parser.parse("Jun 1 2010  1:33PM")
    # "01-01T01:00:00"
    w = world.weather.get_weather(time_test.timestamp())

    a = 1
    print(world_utils.milliseconds_convert(1000 * 10 * 60))
