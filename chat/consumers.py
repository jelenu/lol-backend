from channels.generic.websocket import AsyncWebsocketConsumer
import json
import jwt
from django.conf import settings
from django.contrib.auth.models import User
from users.models import FriendRequest
from channels.db import database_sync_to_async
from .models import Message

def get_room_group_name(username1, username2):
    # Function to generate a unique room name based on sorted usernames
    sorted_usernames = sorted([username1, username2])
    return f"chat_{sorted_usernames[0]}_{sorted_usernames[1]}"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Establish WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        
        if 'type' in text_data_json:
            message_type = text_data_json['type']
            
            if message_type == 'auth':
                # Authentication message type
                token = text_data_json.get('token')
                if token:
                    self.user = await self.get_user_from_token(token)
                    if not self.user:
                        # Close connection if user is not authenticated
                        await self.close()
                        return

                    self.username1 = self.scope['url_route']['kwargs']['username1']
                    self.username2 = self.scope['url_route']['kwargs']['username2']

                    if self.user.username not in [self.username1, self.username2]:
                        # Close connection if user is not part of the chat
                        await self.close()
                        return

                    user1 = await self.get_user(self.username1)
                    user2 = await self.get_user(self.username2)

                    if not await self.are_friends(user1, user2):
                        # Close connection if users are not friends
                        await self.close()
                        return

                    self.room_group_name = get_room_group_name(self.username1, self.username2)
                    await self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name
                    )

                    history = await self.get_chat_history(user1, user2)
                    messages = [
                        {
                            'message': message.content,
                            'sender': await self.get_username(message.sender_id),
                            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        for message in history
                    ]
                    await self.send(text_data=json.dumps({'history': messages}))
                else:
                    print("Token not found in auth message")
                    await self.close()
            elif message_type == 'message':
                # Message type
                if 'message' in text_data_json:
                    message_content = text_data_json['message']
                    user1 = await self.get_user(self.username1)
                    user2 = await self.get_user(self.username2)
                    sender = self.user
                    receiver = user2 if sender == user1 else user1

                    message = await self.save_message(sender, receiver, message_content)

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': message.content,
                            'sender': await self.get_username(message.sender_id),
                            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
                else:
                    print("Missing 'message' key in message data")
        else:
            print("Missing 'type' key in message data")

    async def chat_message(self, event):
        # Send chat message to WebSocket
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def get_user(self, username):
        # Retrieve user object asynchronously
        return User.objects.get(username=username)

    @database_sync_to_async
    def are_friends(self, user1, user2):
        # Check if users are friends asynchronously
        return FriendRequest.objects.filter(sender=user1, receiver=user2, accepted=True).exists() or FriendRequest.objects.filter(sender=user2, receiver=user1, accepted=True).exists()

    @database_sync_to_async
    def get_chat_history(self, user1, user2):
        # Retrieve chat history between two users asynchronously
        return list(Message.objects.filter(sender__in=[user1, user2], receiver__in=[user1, user2]).order_by('timestamp'))

    @database_sync_to_async
    def save_message(self, sender, receiver, content):
        # Save message asynchronously
        return Message.objects.create(sender=sender, receiver=receiver, content=content)

    @database_sync_to_async
    def get_username(self, user_id):
        # Retrieve username asynchronously
        return User.objects.get(id=user_id).username

    @database_sync_to_async
    def get_user_from_token(self, token):
        # Retrieve user from JWT token asynchronously
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            return user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return None
