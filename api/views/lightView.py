import json

from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from random import randrange, getrandbits

from sim.home import Light
from sim.world import *

class HouseLightView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        print(localBuilding.rooms[0].light)
        sumLights = sum(map(lambda room: 1 if room.light else 0, localBuilding.rooms))
        obj = dict()
        obj['houseTurnedLights'] = sumLights

        return JsonResponse(obj)


class LightView(generics.RetrieveUpdateAPIView):
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        if 'roomId' not in kwargs or kwargs['roomId'] > len(localBuilding.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        roomId = kwargs['roomId']
        room = localBuilding.rooms[roomId]

        obj = dict()
        obj['roomId'] = roomId
        # obj['light'] = room.light
        lights = []
        for l in room.lights:
            light = {'id': l.id,'name': l.name, 'state': l.on}
            lights.append(light)
        # lights = [x for x in room.lights]
        obj['lights'] = lights

        return JsonResponse(obj)

    def put(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        if 'roomId' not in kwargs or kwargs['roomId'] > len(localBuilding.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')
        if 'lightId' not in request.query_params:
            return HttpResponseBadRequest('<h1>Bad light id</h1>')
        if 'state' not in request.query_params:
            return HttpResponseBadRequest('<h1>Bad light state</h1>')

        # if 'setLight' not in request.data or request.data['setLight'] not in ['true', 'false']:
        #     return HttpResponseBadRequest('<h1>Set light state out of range</h1>')

        roomId = kwargs['roomId']
        state = request.query_params['state'] == 'true'
        room = localBuilding.rooms[roomId]
        # TODO DEBUG
        # lightId = str(room.lights[0].id)
        lightId = request.query_params['lightId']
        lights = [x for x in room.lights if str(x.id) == lightId]
        if len(lights) == 1:
            light = lights[0]
            light.on = state
            world.state.building = localBuilding
            return HttpResponse('', status=200)
        else:
            return HttpResponseBadRequest('<h1>Bad light id</h1>')


class HouseLightHistoryView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):

        if 'nlast' not in kwargs:
            return HttpResponseNotFound('<h1>Number of elements is out of range</h1>')

        obj = dict()
        obj['lightHistory'] = [bool(getrandbits(1)) for i in range(0, kwargs['nlast'])]

        return JsonResponse(obj)


class LightHistoryView(generics.RetrieveAPIView):
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



