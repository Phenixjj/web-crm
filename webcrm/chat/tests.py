from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Chat, Message

# Get the User model from Django's built-in authentication system
User = get_user_model()


# This class is used to test the Message model
class MessageModelTest(TestCase):
    # This method is called before each test case
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username="user1", password="testpass123")
        self.user2 = User.objects.create_user(username="user2", password="testpass123")
        # Create a chat and add the two users as participants
        self.chat = Chat.objects.create()
        self.chat.participants.add(self.user1, self.user2)
        # Create a message in the chat from user1
        self.message = Message.objects.create(
            author=self.user1, chat_room=self.chat, content="Hello, World!"
        )

    # This test case checks if the content of the message is correct
    def test_message_content(self):
        self.assertEqual(f"{self.message.content}", "Hello, World!")

    # This test case checks if the author of the message is correct
    def test_message_author(self):
        self.assertEqual(f"{self.message.author.username}", "user1")

    # This test case checks if the chat room of the message is correct
    def test_message_chat_room(self):
        self.assertEqual(
            f"{self.message.chat_room}", f"{self.user1.username}, {self.user2.username}"
        )

    # This test case checks if the last_10_messages method returns the correct number of messages
    def test_last_10_messages(self):
        # Create 15 messages in the chat from user1
        for i in range(15):
            Message.objects.create(
                author=self.user1, chat_room=self.chat, content=f"Message {i}"
            )
        # Check if the last_10_messages method returns 10 messages
        self.assertEqual(len(Message.last_10_messages()), 10)
