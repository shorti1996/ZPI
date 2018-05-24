from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from random import randrange
from sim.world import *

class HouseTemperatureView(generics.RetrieveAPIView):
    # @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        avgRoomTemps = sum(map(lambda room: room.temperature, localBuilding.rooms)) / len(localBuilding.rooms)
        obj = dict()

        obj['houseTemperature'] = avgRoomTemps

        return JsonResponse(obj)

class TemperatureView(generics.RetrieveUpdateAPIView):
    # @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        if 'roomId' not in kwargs or kwargs['roomId'] > len(localBuilding.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        roomId = kwargs['roomId']
        room = localBuilding.rooms[roomId]

        obj = dict()
        obj['roomId'] = kwargs['roomId']
        obj['temperature'] = room.temperature
        obj['setTemperature'] = room.setTemperature

        return JsonResponse(obj)

    # @api_permission(['UserWithPrivilege'])
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

        print(temperature)
        print(room.setTemperature)
        room.temperature = temperature
        print(room.temperature)
        print(room.setTemperature)
        world.state.building = localBuilding

        return HttpResponse('', status=200)


class HouseTemperatureHistoryView(generics.RetrieveAPIView):
    # @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        obj = dict()

        if 'nlast' not in kwargs:
            return HttpResponseNotFound('<h1>Number of elements is out of range</h1>')

        obj['temperatureHistory'] = [randrange(0, 10) for i in range(0, kwargs['nlast'])]

        return JsonResponse(obj)

class TemperatureHistoryView(generics.RetrieveAPIView):
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
        obj['temperatureHistory'] = [randrange(0, 10) for i in range(0, kwargs['nlast'])]

        return JsonResponse(obj)