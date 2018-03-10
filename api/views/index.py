from rest_framework import generics
from django.http import JsonResponse
from sim.world import *


class IndexView(generics.ListCreateAPIView):
    gen = get_weather_hourly()

    def get(self, request, *args, **kwargs):
        obj = gen.__next__()

        return JsonResponse(obj)

