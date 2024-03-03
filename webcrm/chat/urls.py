from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.chat_lobby, name="lobby"),
    path("create_chat/", views.create_chat, name="create_chat"),
    re_path(r'^(?P<room_name>\S+)/$', views.room, name='chat_room'),
]
