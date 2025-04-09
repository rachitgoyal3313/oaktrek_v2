# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = f"chat_{self.scope['url_route']['kwargs']['chat_key']}"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_username = data['sender']
        receiver_username = data['receiver']

        sender = await self.get_user(sender_username)
        receiver = await self.get_user(receiver_username)

        # Save to DB
        await self.save_message(sender, receiver, message)

        # Broadcast to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @staticmethod
    async def get_user(username):
        return await sync_to_async(User.objects.get)(username=username)

    @staticmethod
    async def save_message(sender, receiver, message):
        await sync_to_async(Message.objects.create)(
            sender=sender,
            receiver=receiver,
            content=message
        )

from asgiref.sync import sync_to_async
