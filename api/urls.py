from django.urls import include, path
from api.views.index import *

urlpatterns = [
    path('', IndexView.as_view()),
]