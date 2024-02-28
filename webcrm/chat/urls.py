from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    re_path(r'^(?P<room_name>\S+)/$', views.room, name='room'),
]
