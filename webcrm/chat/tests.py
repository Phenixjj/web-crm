from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Chat, Message

User = get_user_model()


class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        self.chat = Chat.objects.create()
        self.chat.participants.add(self.user1, self.user2)
        self.message = Message.objects.create(author=self.user1, chat_room=self.chat, content="Hello, World!")

    def test_message_content(self):
        self.assertEqual(f'{self.message.content}', 'Hello, World!')

    def test_message_author(self):
        self.assertEqual(f'{self.message.author.username}', 'user1')

    def test_message_chat_room(self):
        self.assertEqual(f'{self.message.chat_room}', f'{self.user1.username}, {self.user2.username}')

    def test_last_10_messages(self):
        for i in range(15):
            Message.objects.create(author=self.user1, chat_room=self.chat, content=f"Message {i}")
        self.assertEqual(len(Message.last_10_messages()), 10)