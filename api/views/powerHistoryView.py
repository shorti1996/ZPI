from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from random import randrange, getrandbits
from sim.world import *
from api.api_permission import api_permission
from sim.models import *


class HousePowerHistoryView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        if 'nlast' not in kwargs:
            return HttpResponseNotFound('<h1>Number of elements is out of range</h1>')

        timestamps = list(reversed(list(map(lambda value: value['timestamp'],
                          PowerHistory.objects.order_by('-timestamp').values('timestamp').distinct()[:kwargs['nlast']]))))

        powerObjects = PowerHistory.objects.filter(timestamp__in=timestamps)

        obj = {
            'houseLightPowerHistory': list(map(lambda timestamp: sum(map(lambda power: power.lightValue, filter(lambda power: power.timestamp == timestamp, powerObjects))), timestamps)),
            'houseClimatPowerHistory': list(map(lambda timestamp: sum(map(lambda power: power.climatValue, filter(lambda power: power.timestamp == timestamp, powerObjects))), timestamps)),
        }

        return JsonResponse(obj)


class PowerHistoryView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()
        localBuilding = world.state.building

        if 'roomId' not in kwargs or kwargs['roomId'] > len(localBuilding.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        if 'nlast' not in kwargs:
            return HttpResponseNotFound('<h1>Number of elements is out of range</h1>')

        roomId = kwargs['roomId']

        timestamps = list(reversed(list(map(lambda value: value['timestamp'],
                                            PowerHistory.objects.order_by('-timestamp').values('timestamp').distinct()[
                                            :kwargs['nlast']]))))

        powerObjects = PowerHistory.objects.filter(timestamp__in=timestamps, room_id=roomId)

        obj = {
            'roomId': roomId,
            'lightPowerHistory': list(map(lambda timestamp: sum(
                map(lambda power: power.lightValue, filter(lambda power: power.timestamp == timestamp, powerObjects))),
                                        timestamps)),
            'climatPowerHistory': list(map(lambda timestamp: sum(
                map(lambda power: power.climatValue, filter(lambda power: power.timestamp == timestamp, powerObjects))),
                                                timestamps)),
        }

        return JsonResponse(obj)
