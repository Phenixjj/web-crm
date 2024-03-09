from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.chat_lobby, name="lobby"),
    path("create_chat/", views.create_chat, name="create_chat"),
    re_path(r"^(?P<room_name>\S+)/$", views.room, name="chat_room"),
    path("get_token/", views.getToken),
    path("create_member/", views.createMember),
    path("get_member/", views.getMember),
    path("delete_member/", views.deleteMember),
]
