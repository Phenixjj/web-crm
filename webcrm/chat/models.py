from django.contrib.auth import get_user_model
from django.db import models

# Get the User model from Django's built-in authentication system
User = get_user_model()


# Chat model represents a chat room
class Chat(models.Model):
    # room_name is the name of the chat room
    room_name = models.CharField(max_length=100, null=True, blank=True)
    # participants are the users participating in the chat
    participants = models.ManyToManyField(User, related_name="chats")

    def __str__(self):
        # Returns a string representation of the chat room, listing all participants
        return ", ".join([str(participant) for participant in self.participants.all()])


# Message model represents a message in a chat room
class Message(models.Model):
    # author is the user who sent the message
    author = models.ForeignKey(
        User, related_name="author_messages", on_delete=models.CASCADE
    )
    # chat_room is the chat room where the message was sent
    chat_room = models.ForeignKey(
        Chat,
        related_name="chat_messages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # content is the text of the message
    content = models.TextField()
    # timestamp is the time when the message was sent
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Returns a string representation of the message, showing the author's username
        return self.author.username

    @staticmethod
    def last_10_messages():
        # Returns the last 10 messages, ordered by timestamp
        return Message.objects.order_by("-timestamp").all()[:10]


# RoomMember model represents a member of a chat room
class RoomMember(models.Model):
    # name is the name of the member
    name = models.CharField(max_length=200)
    # uid is a unique identifier for the member
    uid = models.CharField(max_length=1000)
    # room_name is the name of the chat room the member is in
    room_name = models.CharField(max_length=200)
    # insession indicates whether the member is currently in the chat room
    insession = models.BooleanField(default=True)

    def __str__(self):
        # Returns a string representation of the room member, showing their name
        return self.name
