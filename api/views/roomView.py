from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from random import randrange
from sim.world import *
from api.api_permission import *


class RoomView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        obj = {
            'rooms': list(map(lambda room: {'roomId': room.id, 'name': room.name}, localBuilding.rooms))
        }
        return JsonResponse(obj)

class RoomDetailView(generics.RetrieveAPIView):
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
            'roomName': room.name,
            'roomVolume': room.volume,
        }

        return JsonResponse(obj)