from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from random import randrange, getrandbits
from sim.world import *
from api.api_permission import api_permission


class HousePowerView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        obj = {
            'houseLightPower': sum(map(lambda room: sum(map(lambda light: light.power, room.lights.values())), localBuilding.rooms)),
            'houseClimatPower': sum(map(lambda room: abs(room.hvac.power), localBuilding.rooms)),
        }

        return JsonResponse(obj)


class PowerView(generics.RetrieveAPIView):
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
            'lightPower': sum(map(lambda light: light.power, room.lights.values())),
            'climatPower': room.hvac.power,
        }

        return JsonResponse(obj)
