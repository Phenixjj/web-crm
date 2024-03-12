import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model

from .models import Chat, Message

# Get the user model
User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    """
    A consumer that handles websocket connections for chat rooms.
    """

    def fetch_messages(self, data):
        """
        Fetch the last 10 messages from the chat room specified in the data.

        :param data: The data received from the websocket
        :type data: dict
        """
        room_name = data.get("room_name")  # Get the room_name from the data
        if room_name:
            try:
                chat = Chat.objects.get(room_name=room_name)
                messages = chat.chat_messages.order_by("-timestamp")[
                    :10
                ]  # Get the last 10 messages
                # reverse the order of the last 10 message to get the correct order
                messages = messages[::-1]
                content = {
                    "command": "messages",
                    "messages": self.messages_to_json(messages),
                }
                self.send_message(content)
            except Chat.DoesNotExist:
                # Handle the case where the chat room doesn't exist
                error_message = {
                    "command": "error",
                    "error": f"Chat room '{room_name}' not found.",
                }
                self.send_message(error_message)
        else:
            # Handle the case where room_name is not provided
            error_message = {
                "command": "error",
                "error": "Room name is required to fetch messages.",
            }
            self.send_message(error_message)

    def new_message(self, data):
        """
        Create a new message in the chat room.

        :param data: The data received from the websocket
        :type data: dict
        """
        author = data["from"]
        author_user = User.objects.get(username=author)
        room_name = self.scope["url_route"]["kwargs"]["room_name"]

        chat_room = Chat.objects.get(room_name=room_name)

        message = Message.objects.create(
            author=author_user, content=data["message"], chat_room=chat_room
        )
        content = {
            "command": "new_message",
            "message": self.message_to_json(message),
        }
        self.send_chat_message(content)

    def messages_to_json(self, messages):
        """
        Convert a list of messages to JSON format.

        :param messages: The messages to convert
        :type messages: list
        :return: The messages in JSON format
        :rtype: list
        """
        return [self.message_to_json(message) for message in messages]

    @staticmethod
    def message_to_json(message):
        """
        Convert a message to JSON format.

        :param message: The message to convert
        :type message: Message
        :return: The message in JSON format
        :rtype: dict
        """
        return {
            "author": message.author.username,
            "content": message.content,
            "timestamp": str(message.timestamp),
        }

    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message,
    }

    def connect(self):
        """
        Handle a new websocket connection.
        """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        """
        Handle a websocket disconnection.

        :param close_code: The close code of the disconnection
        :type close_code: int
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        """
        Handle data received from the websocket.

        :param text_data: The data received from the websocket
        :type text_data: str
        """
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        """
        Send a chat message to the websocket.

        :param message: The message to send
        :type message: dict
        """
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message,
            },
        )

    def send_message(self, message):
        """
        Send a message to the websocket.

        :param message: The message to send
        :type message: dict
        """
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        """
        Handle a chat message event.

        :param event: The event data
        :type event: dict
        """
        message = event["message"]
        self.send(text_data=json.dumps(message))
