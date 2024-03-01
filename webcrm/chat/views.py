import json

from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.shortcuts import render

# Create your views here.


def chat_lobby(request):
    return render(request, "chat/chat.html")


@login_required
def room(request, room_name):
    return render(request, "chat/room.html", {
        "room_name": room_name,
        "username": mark_safe(json.dumps(request.user.username)),
    })
