from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from random import randrange
from sim.world import *
from api.api_permission import *


class HouseTemperatureView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()

        obj = {
            'houseTemperature': sum(map(lambda room: room.temperature, world.state.building.rooms)) / len(world.state.building.rooms)
        }

        return JsonResponse(obj)


class OutsideTemperatureView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()

        obj = {
            'temperature': world.state.building.outside.temperature,
        }

        return JsonResponse(obj)



class TemperatureView(generics.RetrieveUpdateAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()

        if 'roomId' not in kwargs or kwargs['roomId'] > len(world.state.building.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        roomId = kwargs['roomId']
        room = world.state.building.rooms[roomId]

        obj = {
            'roomId': kwargs['roomId'],
            'temperature': room.temperature,
            'setTemperature': room.setTemperature
        }
        return JsonResponse(obj)

    @api_permission(['Owner'])
    def put(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        if 'roomId' not in kwargs or kwargs['roomId'] > len(localBuilding.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        if 'setTemperature' not in request.data or not 10 <= int(request.data['setTemperature']) <= 35:
            return HttpResponseBadRequest('<h1>Set temperature out of range</h1>')

        roomId = kwargs['roomId']
        temperature = int(request.data['setTemperature'])
        room = localBuilding.rooms[roomId]

        room.temperature = temperature
        world.state.building = localBuilding

        return HttpResponse('', status=200)
