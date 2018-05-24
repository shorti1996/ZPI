from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from random import randrange, getrandbits
from sim.world import *
from api.api_permission import api_permission


class HouseLightView(generics.RetrieveAPIView):
    # @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        print(localBuilding.rooms[0].light)
        sumLights = sum(map(lambda room: 1 if room.light else 0, localBuilding.rooms))
        obj = dict()
        obj['houseTurnedLights'] = sumLights

        return JsonResponse(obj)


class LightView(generics.RetrieveUpdateAPIView):
    # @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        if 'roomId' not in kwargs or kwargs['roomId'] > len(localBuilding.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        roomId = kwargs['roomId']
        room = localBuilding.rooms[roomId]

        obj = dict()
        obj['roomId'] = roomId
        obj['light'] = room.light

        return JsonResponse(obj)

    # @api_permission(['UserWithPrivilege'])
    def put(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        if 'roomId' not in kwargs or kwargs['roomId'] > len(localBuilding.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        if 'setLight' not in request.data or request.data['setLight'] not in ['true', 'false']:
            return HttpResponseBadRequest('<h1>Set light state out of range</h1>')

        roomId = kwargs['roomId']
        state = request.data['setLight'] == 'true'
        room = localBuilding.rooms[roomId]

        room.light = state
        world.state.building = localBuilding

        return HttpResponse('', status=200)


class HouseLightHistoryView(generics.RetrieveAPIView):
    # @api_permission(['User'])
    def get(self, request, *args, **kwargs):

        if 'nlast' not in kwargs:
            return HttpResponseNotFound('<h1>Number of elements is out of range</h1>')

        obj = dict()
        obj['lightHistory'] = [bool(getrandbits(1)) for i in range(0, kwargs['nlast'])]

        return JsonResponse(obj)


class LightHistoryView(generics.RetrieveAPIView):
    # @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        if 'roomId' not in kwargs or kwargs['roomId'] > len(localBuilding.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        if 'nlast' not in kwargs:
            return HttpResponseNotFound('<h1>Number of elements is out of range</h1>')

        obj = dict()
        obj['roomId'] = kwargs['roomId']
        obj['lightHistory'] = [bool(getrandbits(1)) for i in range(0, kwargs['nlast'])]

        return JsonResponse(obj)



