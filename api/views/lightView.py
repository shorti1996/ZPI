from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from random import randrange, getrandbits
from sim.world import *
from api.api_permission import api_permission


class HouseLightView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()

        obj = {
            'houseTurnedLights': sum(map(lambda room: sum(map(lambda light: 1 if light.state else 0, room.lights.values())), world.state.building.rooms)),
            'lights': list(map(lambda room: list(map(lambda light: {'id': light.id, 'name': light.name, 'state': light.state}, room.lights.values())), world.state.building.rooms)),
        }

        return JsonResponse(obj)


class LightView(generics.RetrieveUpdateAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()

        if 'roomId' not in kwargs or kwargs['roomId'] > len(world.state.building.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        roomId = kwargs['roomId']
        room = world.state.building.rooms[roomId]

        obj = {
            'roomId': roomId,
            'lights': list(map(lambda light: {'id': light.id, 'name': light.name, 'state': light.state}, room.lights.values())),
        }

        return JsonResponse(obj)

    @api_permission(['Owner'])
    def put(self, request, *args, **kwargs):
        world = World()

        if 'roomId' not in kwargs or kwargs['roomId'] > len(world.state.building.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        if 'lightId' not in request.query_params:
            return HttpResponseBadRequest('<h1>Bad light id</h1>')

        if 'state' not in request.query_params:
            return HttpResponseBadRequest('<h1>Bad light state</h1>')

        roomId = kwargs['roomId']
        state = request.query_params['state'] == 'true'

        world.lock.acquire()
        localBuilding = world.state.building
        room = localBuilding.rooms[roomId]

        lightId = request.query_params['lightId']
        light = room.lights[int(lightId)]

        if not light:
            world.lock.release()
            return HttpResponseBadRequest('<h1>Bad light id</h1>')

        light.state = state

        world.state.building = localBuilding
        world.lock.release()

        return HttpResponse('', status=200)
