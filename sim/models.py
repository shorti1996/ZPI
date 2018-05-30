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
