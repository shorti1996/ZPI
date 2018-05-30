from django.urls import include, path
from api.views.roomView import *
from api.views.lightView import *
from api.views.temperatureView import *
from api.views.powerView import *
from api.views.lightHistoryView import *
from api.views.temperatureHistoryView import *
from api.views.powerHistoryView import *

urlpatterns = [
    path(r'light', HouseLightView.as_view()),
    path(r'light/<int:roomId>', LightView.as_view()),

    path(r'light/history/<int:nlast>', HouseLightHistoryView.as_view()),
    path(r'light/<int:roomId>/history/<int:nlast>', LightHistoryView.as_view()),

    path(r'temp', HouseTemperatureView.as_view()),
    path(r'temp/<int:roomId>', TemperatureView.as_view()),

    path(r'temp/history/<int:nlast>', HouseTemperatureHistoryView.as_view()),
    path(r'temp/<int:roomId>/history/<int:nlast>', TemperatureHistoryView.as_view()),

    path(r'power', HousePowerView.as_view()),
    path(r'power/<int:roomId>', PowerView.as_view()),

    path(r'power/history/<int:nlast>', HousePowerHistoryView.as_view()),
    path(r'power/<int:roomId>/history/<int:nlast>', PowerHistoryView.as_view()),

    path(r'room', RoomView.as_view()),
    path(r'room/<int:roomId>', RoomDetailView.as_view()),
]