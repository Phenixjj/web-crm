import json
import random
import time

from agora_token_builder import RtcTokenBuilder
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from webcrm.env import config

from .models import Chat, RoomMember

# Create your views here.


@login_required
def chat_lobby(request):
    all_users = User.objects.exclude(username=request.user.username)
    user_chats = request.user.chats.all()
    return render(
        request, "chat/chat.html", {"user_chats": user_chats, "all_users": all_users}
    )


@login_required
def create_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        room_name = data.get("room_name")
        participant_usernames = data.get("participants")

        # Check if the room name is provided
        if not room_name:
            return JsonResponse(
                {"success": False, "error": "Room name is required"}, status=400
            )

        # Check if there are participants
        if not participant_usernames:
            return JsonResponse(
                {"success": False, "error": "Participants are required"}, status=400
            )

        # Retrieve the User instances for the provided usernames
        participants = User.objects.filter(username__in=participant_usernames)

        # Create chat room
        chat = Chat.objects.create(room_name=room_name)

        chat.participants.add(request.user)

        # Add participants to the chat room
        chat.participants.add(*participants)  # Unpack participants queryset using *
        chat.save()

        # Redirect to the chat room
        return render(
            request,
            "chat/room.html",
            {
                "room_name": room_name,
                "username": request.user.username,
            },
        )
    else:
        return JsonResponse(
            {"success": False, "error": "Method not allowed"}, status=405
        )


@login_required
def room(request, room_name):
    chat = Chat.objects.get(room_name=room_name)
    last_10_messages = chat.chat_messages.order_by("-timestamp")[:10]

    return render(
        request,
        "chat/room.html",
        {
            "room_name": room_name,
            "username": mark_safe(json.dumps(request.user.username)),
            "last_10_messages": last_10_messages,
        },
    )


def getToken(request):
    appId = str(config("AGORA_APP_ID"))
    appCertificate = str(config("AGORA_APP_CERTIFICATE"))
    channelName = request.GET.get("channel")
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, uid, role, privilegeExpiredTs
    )

    return JsonResponse({"token": token, "uid": uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data["name"], uid=data["UID"], room_name=data["room_name"]
    )

    return JsonResponse({"name": data["name"]}, safe=False)


def getMember(request):
    uid = request.GET.get("UID")
    room_name = request.GET.get("room_name")

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    member.name
    return JsonResponse({"name": member.name}, safe=False)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data["name"], uid=data["UID"], room_name=data["room_name"]
    )
    member.delete()
    return JsonResponse("Member deleted", safe=False)


# def video_chat(request):
#     return render(request, "chat/video_chat.html")
