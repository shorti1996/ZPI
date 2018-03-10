from rest_framework import generics
from django.http import JsonResponse
from sim.world import *


class IndexView(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        gen = get_weather_hourly()
        # print(gen.__next__()["NAME"])

        obj = gen.__next__()

        return JsonResponse(obj)

