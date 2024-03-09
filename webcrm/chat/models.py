from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class Chat(models.Model):
    room_name = models.CharField(max_length=100, null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="chats")

    def __str__(self):
        return ", ".join([str(participant) for participant in self.participants.all()])


class Message(models.Model):
    author = models.ForeignKey(
        User, related_name="author_messages", on_delete=models.CASCADE
    )
    chat_room = models.ForeignKey(
        Chat,
        related_name="chat_messages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    @staticmethod
    def last_10_messages():
        return Message.objects.order_by("-timestamp").all()[:10]


class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name
