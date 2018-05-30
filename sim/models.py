from django.db import models


class TemperatureHistory(models.Model):
    timestamp = models.IntegerField()
    room_id = models.IntegerField()
    value = models.FloatField()


class LightHistory(models.Model):
    timestamp = models.IntegerField()
    room_id = models.IntegerField()
    light_id = models.IntegerField()
    value = models.BooleanField()


class PowerHistory(models.Model):
    timestamp = models.IntegerField()
    room_id = models.IntegerField()
    lightValue = models.IntegerField()
    climatValue = models.IntegerField()
