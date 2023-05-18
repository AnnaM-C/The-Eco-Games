from django.contrib.auth.models import User
from django.test import TestCase, Client
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from chat.consumers import ChatConsumer, ChatRoomConsumer
from chat.routing import websocket_urlpatterns
import json


class ChatTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.room_name = 'test_room'

    def test_chat_view(self):
        response = self.client.get('/chat/test_room/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<textarea id="chat-log"')

    def test_chat_view_requires_authentication(self):
        response = self.client.get('/chat/test_room/')
        self.assertRedirects(response, '/login/?next=/chat/test_room/')

    async def test_chat_consumer(self):
        channel_layer = get_channel_layer()
        communicator = WebsocketCommunicator(websocket_urlpatterns, f'/ws/chat/{self.room_name}/')
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await channel_layer.group_send(
            f'chat_{self.room_name}',
            {'type': 'chat_message', 'message': 'Test message'}
        )

        response = await communicator.receive_json_from()

        self.assertEqual(response['message'], 'Test message')

        await communicator.disconnect()

    async def test_chat_room_consumer(self):
        channel_layer = get_channel_layer()
        communicator = WebsocketCommunicator(websocket_urlpatterns, f'/ws/chatbox/{self.room_name}/')
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await channel_layer.group_send(
            f'chat_{self.room_name}',
            {'type': 'chatbox_message', 'message': 'Test message', 'username': 'testuser'}
        )

        response = await communicator.receive_json_from()

        self.assertEqual(response['message'], 'Test message')
        self.assertEqual(response['username'], 'testuser')

        await communicator.disconnect()
