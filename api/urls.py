from django.urls import include, path
from api.views.index import *
from api.views.lightView import *
from api.views.temperatureView import *

urlpatterns = [
    path(r'', IndexView.as_view()),
    path(r'temp/<int:roomId>', TemperatureView.as_view()),
    path(r'temp/<int:roomId>/hist/<int:nlast>', TemperatureHistoryView.as_view()),
    path(r'light/<int:roomId>', LightView.as_view()),
    path(r'light/<int:roomId>/hist/<int:nlast>', LightHistoryView.as_view()),
]