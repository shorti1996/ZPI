from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from random import randrange
from sim.world import *


class RoomView(generics.RetrieveAPIView):
    # @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        obj = dict()
        obj['rooms'] = []
        for i in range(0, len(localBuilding.rooms)):
            room = localBuilding.rooms[i]
            obj['rooms'].append({'roomId': i, 'name': room.name})

        return JsonResponse(obj)

class RoomDetailView(generics.RetrieveAPIView):
    # @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        if 'roomId' not in kwargs or kwargs['roomId'] > len(localBuilding.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        obj = dict()

        roomId = kwargs['roomId']
        room = localBuilding.rooms[roomId]

        obj['roomId'] = roomId
        obj['roomName'] = room.name
        obj['roomVolume'] = room.volume

        return JsonResponse(obj)