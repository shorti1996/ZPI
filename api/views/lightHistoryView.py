from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from random import randrange, getrandbits
from sim.world import *
from api.api_permission import api_permission
from sim.models import *


class HouseLightHistoryView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        if 'nlast' not in kwargs:
            return HttpResponseNotFound('<h1>Number of elements is out of range</h1>')

        timestamps = list(reversed(list(map(lambda value: value['timestamp'],
                          LightHistory.objects.order_by('-timestamp').values('timestamp').distinct()[:kwargs['nlast']]))))

        lightObjects = LightHistory.objects.filter(timestamp__in=timestamps)

        obj = {
            'houseTurnedLights': list(map(lambda timestamp: sum(map(lambda light: 1 if light.value else 0, filter(lambda light: light.timestamp == timestamp, lightObjects))), timestamps)),
        }

        return JsonResponse(obj)


class LightHistoryView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        if 'roomId' not in kwargs or kwargs['roomId'] > len(localBuilding.rooms) - 3:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        if 'lightId' not in request.query_params:
            return HttpResponseBadRequest('<h1>Bad light id</h1>')

        if 'nlast' not in kwargs:
            return HttpResponseNotFound('<h1>Number of elements is out of range</h1>')

        roomId = kwargs['roomId']
        room = localBuilding.rooms[roomId]

        lightId = request.query_params['lightId']
        light = room.lights[int(lightId)]

        if not light:
            return HttpResponseBadRequest('<h1>Bad light id</h1>')

        timestamps = list(reversed(list(map(lambda value: value['timestamp'],
                          LightHistory.objects.order_by('-timestamp')
                          .values('timestamp').distinct()[:kwargs['nlast']]))))

        lightObjects = LightHistory.objects.filter(timestamp__in=timestamps, light_id=light.id)

        obj = {
            'roomId': roomId,
            'id': light.id,
            'name': light.name,
            'lightHistory': list(map(lambda timestamp: 'true' if list(filter(lambda light: light.timestamp == timestamp, lightObjects))[0].value else 'false', timestamps)),
        }

        return JsonResponse(obj)
