import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.shortcuts import render
from .models import Chat

# Create your views here.


@login_required
def chat_lobby(request):
    all_users = User.objects.exclude(username=request.user.username)
    user_chats = request.user.chats.all()
    return render(request, "chat/chat.html", {'user_chats': user_chats, 'all_users': all_users})


@login_required
def create_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        room_name = data.get('room_name')
        participant_usernames = data.get('participants')

        # Check if the room name is provided
        if not room_name:
            return JsonResponse({'success': False, 'error': 'Room name is required'}, status=400)

        # Check if there are participants
        if not participant_usernames:
            return JsonResponse({'success': False, 'error': 'Participants are required'}, status=400)

        # Retrieve the User instances for the provided usernames
        participants = User.objects.filter(username__in=participant_usernames)

        # Create chat room
        chat = Chat.objects.create(room_name=room_name)

        chat.participants.add(request.user)

        # Add participants to the chat room
        chat.participants.add(*participants)  # Unpack participants queryset using *
        chat.save()

        # Redirect to the chat room
        return render(request, "chat/room.html", {
            "room_name": room_name,
            "username": request.user.username,
        })
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


@login_required
def room(request, room_name):
    chat = Chat.objects.get(room_name=room_name)
    last_10_messages = chat.chat_messages.order_by('-timestamp')[:10]

    return render(request, "chat/room.html", {
        "room_name": room_name,
        "username": mark_safe(json.dumps(request.user.username)),
        "last_10_messages": last_10_messages,
    })
