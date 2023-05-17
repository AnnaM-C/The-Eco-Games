from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.test import TestCase
from channels.testing import WebsocketCommunicator
from chat.consumers import ChatRoomConsumer
from theEcoGames.routing import application

class ChatTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='ecogames')
        self.room = 'General'
        self.url = f'/ws/chat/{self.room}/'
    
    async def test_chat_consumer(self):
        communicator = WebsocketCommunicator(ChatRoomConsumer.as_asgi(), self.url)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
    
        # Send a message
        message = {'message': self.user + ": " + "Hello"}
        await communicator.send_json_to(message)

        # Receive the message
        response = await communicator.receive_json_from()

        # Check if the received message matches
        self.assertEqual(response['message'], f'{self.user.username}: Hello!')

        # Disconnect
        await communicator.disconnect()

    def test_chat_view(self):
        # Log in the user
        self.client.login(username='admin', password='ecogames')

        # Access the chat view
        response = self.client.get('/chat/test_room/')

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_room')
        self.assertContains(response, self.user.username)

        # Check if the necessary HTML elements exist
        self.assertContains(response, '<textarea id="chat-log"')
        self.assertContains(response, '<input id="chat-message-input"')
        self.assertContains(response, '<input id="chat-message-submit"')

    def test_chat_view_requires_authentication(self):
        # Log out the user
        self.client.logout()

        # Attempt to access the chat view
        response = self.client.get('/chat/test_room/')

        # Check if the response is a redirect to the login page
        self.assertRedirects(response, '/login/?next=/chat/test_room/')

    # Add more tests as needed

