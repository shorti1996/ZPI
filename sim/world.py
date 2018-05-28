import csv
import time
from dateutil import parser
from datetime import datetime
from sim import world_utils, physics
import collections
import bisect




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

    def __init__(self):
        self.weather = WeatherCsv('sim/weather_data.csv')
        self.soil = SoilCsv('sim/soil_data.csv')


class Weather:
    """
    Static keys for returning similar dicts for different implementations
    """
    TEMP = "temp"

    def get_weather(self, timestamp):
        raise NotImplementedError("You must implement __get_weather__")


class WeatherCsv(Weather):
    DATE_FMT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, filename):
        (self.weather_data, self.weather_data_keys) = self.load_weather_data(filename)

    @staticmethod
    def load_weather_data(filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = collections.OrderedDict()
            for row in reader:
                date_time = datetime.strptime("2017-" + row["DATE"], WeatherCsv.DATE_FMT).timestamp()
                data[date_time] = row
            return data, list(data.keys())

    def get_weather(self, timestamp):
        index = bisect.bisect_left(self.weather_data_keys, timestamp)
        return self.weather_from_row(self.weather_data[self.weather_data_keys[index]])

    @staticmethod
    def weather_from_row(row):
        result = dict()
        result[Weather.TEMP] = physics.fahrenheitDegreeToCelcius(float(row["HLY-TEMP-NORMAL"]))
        return result


class Soil:
    """
    Static keys for returning similar dicts for different implementations
    """
    TEMP = "temp"

    def get_soil(self, timestamp):
        raise NotImplementedError("You must implement __get_soil__")


class SoilCsv(Soil):
    DATE_FMT = "%Y-%m-%d"

    def __init__(self, filename):
        self.soil_data, self.soil_data_keys = self.load_soil_data(filename)

    @staticmethod
    def load_soil_data(filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = collections.OrderedDict()
            for row in reader:
                date_time = datetime.strptime(row["date"], SoilCsv.DATE_FMT).timestamp()
                data[date_time] = row
            return data, list(data.keys())

    def get_soil(self, timestamp):
        index = bisect.bisect_left(self.soil_data_keys, timestamp)
        return self.soil_from_row(self.soil_data[self.soil_data_keys[index]])

    @staticmethod
    def soil_from_row(row):
        result = dict()
        result[Weather.TEMP] = physics.fahrenheitDegreeToCelcius(float(row["value"]))
        return result

