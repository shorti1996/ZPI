from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound
from random import randrange
from sim.world import *

class LightView(generics.RetrieveUpdateAPIView):
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building
        roomId = kwargs['roomId']
        if roomId > len(localBuilding.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        obj = dict()
        obj['roomId'] = kwargs['roomId']
        obj['light'] = localBuilding.rooms[roomId].light

        return JsonResponse(obj)

    def put(self, request, *args, **kwargs):
        # TODO (mkarol) add setting room light
        pass

class LightHistoryView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        obj = dict()

        obj['roomId'] = kwargs['roomId']
        obj['lightHistory'] = [randrange(0, 10) for i in range(0, kwargs['nlast'])]

        return JsonResponse(obj)
