from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound
from random import randrange
from sim.world import *

class TemperatureView(generics.RetrieveUpdateAPIView):
    def get(self, request, *args, **kwargs):
        world = World()
        state = world.state
        roomId = kwargs['roomId']
        if roomId > len(state.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        obj = dict()
        obj['roomId'] = kwargs['roomId']
        obj['light'] = state.rooms[roomId]['currentTemperature']

        return JsonResponse(obj)

    def put(self, request, *args, **kwargs):
        # TODO (mkarol) add setting room temperature
        pass

class TemperatureHistoryView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        obj = dict()

        obj['roomId'] = kwargs['roomId']
        obj['temperatureHistory'] = [randrange(0, 10) for i in range(0, kwargs['nlast'])]

        return JsonResponse(obj)
