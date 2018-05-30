from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from random import randrange
from sim.world import *
from api.api_permission import *


class RoomView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()

        obj = {
            'rooms': list(map(lambda room: {'roomId': room.id, 'name': room.name}, world.state.building.rooms))
        }
        return JsonResponse(obj)

class RoomDetailView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()

        if 'roomId' not in kwargs or kwargs['roomId'] > len(world.state.building.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        roomId = kwargs['roomId']
        room = world.state.building.rooms[roomId]

        obj = {
            'roomId': roomId,
            'roomName': room.name,
            'roomVolume': room.volume,
        }

        return JsonResponse(obj)