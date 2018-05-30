from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from random import randrange, getrandbits
from sim.world import *
from api.api_permission import api_permission


class HouseLightView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        obj = {
            'houseTurnedLights': sum(map(lambda room: sum(map(lambda light: 1 if light.state else 0, room.lights.values())), localBuilding.rooms)),
            'lights': list(map(lambda room: list(map(lambda light: {'id': light.id, 'name': light.name, 'state': light.state}, room.lights.values())), localBuilding.rooms)),
        }

        return JsonResponse(obj)


class LightView(generics.RetrieveUpdateAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        if 'roomId' not in kwargs or kwargs['roomId'] > len(localBuilding.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        roomId = kwargs['roomId']
        room = localBuilding.rooms[roomId]

        obj = {
            'roomId': roomId,
            'lights': list(map(lambda light: {'id': light.id, 'name': light.name, 'state': light.state}, room.lights.values())),
        }

        return JsonResponse(obj)

    @api_permission(['Owner'])
    def put(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        if 'roomId' not in kwargs or kwargs['roomId'] > len(localBuilding.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        if 'lightId' not in request.query_params:
            return HttpResponseBadRequest('<h1>Bad light id</h1>')

        if 'state' not in request.query_params:
            return HttpResponseBadRequest('<h1>Bad light state</h1>')

        roomId = kwargs['roomId']
        state = request.query_params['state'] == 'true'
        room = localBuilding.rooms[roomId]

        lightId = request.query_params['lightId']
        light = room.lights[int(lightId)]

        if not light:
            return HttpResponseBadRequest('<h1>Bad light id</h1>')

        light.state = state
        world.state.building = localBuilding

        return HttpResponse('', status=200)
