from rest_framework import generics
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from random import randrange
from sim.world import *
from api.api_permission import *
from sim.models import *

class HouseTemperatureHistoryView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):

        if 'nlast' not in kwargs:
            return HttpResponseNotFound('<h1>Number of elements is out of range</h1>')

        timestamps = list(reversed(list(map(lambda value: value['timestamp'],
                              TemperatureHistory.objects.order_by('-timestamp').values('timestamp').distinct()[:kwargs['nlast']]))))

        temperatureObjects = TemperatureHistory.objects.filter(timestamp__in=timestamps)

        obj = {
            'temperatureHistory': list(map(lambda timestamp:
                                           sum(map(lambda temperature: temperature.value,
                                                filter(lambda temperature: temperature.timestamp == timestamp, temperatureObjects))) / len(list(filter(lambda temperature: temperature.timestamp == timestamp, temperatureObjects))),
                                           timestamps)),
        }
        return JsonResponse(obj)


class OutsideTemperatureHistoryView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()

        if 'nlast' not in kwargs:
            return HttpResponseNotFound('<h1>Number of elements is out of range</h1>')

        timestamps = list(reversed(list(map(lambda value: value['timestamp'],
                              TemperatureHistory.objects.filter(room_id=world.state.building.outside.id).order_by('-timestamp').values('timestamp').distinct()[:kwargs['nlast']]))))

        temperatureObjects = TemperatureHistory.objects.filter(timestamp__in=timestamps, room_id=world.state.building.outside.id)

        obj = {
            'temperatureHistory': list(map(lambda timestamp: list(filter(lambda temperature: temperature.timestamp == timestamp, temperatureObjects))[0].value, timestamps)),
        }
        return JsonResponse(obj)


class TemperatureHistoryView(generics.RetrieveAPIView):
    @api_permission(['User'])
    def get(self, request, *args, **kwargs):
        world = World()

        if 'roomId' not in kwargs or kwargs['roomId'] > len(world.state.building.rooms) - 1:
            return HttpResponseNotFound('<h1>Room number is out of range</h1>')

        if 'nlast' not in kwargs:
            return HttpResponseNotFound('<h1>Number of elements is out of range</h1>')

        roomId = kwargs['roomId']

        timestamps = list(reversed(list(map(lambda value: value['timestamp'],
                              LightHistory.objects.order_by('-timestamp')
                              .values('timestamp').distinct()[:kwargs['nlast']]))))

        temperatureObjects = TemperatureHistory.objects.filter(timestamp__in=timestamps, room_id=roomId)

        obj = {
            'roomId': roomId,
            'temperatureHistory': list(map(lambda timestamp: list(filter(lambda temperature: temperature.timestamp == timestamp, temperatureObjects))[0].value, timestamps)),
        }
        return JsonResponse(obj)
