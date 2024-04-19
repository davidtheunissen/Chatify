from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json
from .models import *

class RoomConsumer(WebsocketConsumer):
    # Connect user to group
    def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.chatroom = get_object_or_404(Chatroom, name=self.room_name)
        
        # Add user to group channel layer method
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name
        )
        
        # Update online users' count and add user from 'userOnline' list
        if self.user not in self.chatroom.usersOnline.all():
            self.chatroom.usersOnline.add(self.user)
            self.update_online_count()
            self.chatroom.save()
            
        
        self.accept()
        
        
    # Disconnect user from group
    def disconnect(self, close_code):
        # Remove user from group channel layer method
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )
        
        # Update online users' count and remove user from 'userOnline' list
        if self.user in self.chatroom.usersOnline.all():
            self.chatroom.usersOnline.remove(self.user)
            self.update_online_count()
            
        
    # Receive message on group and broadcast
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        
        # Create message instance and populate its fields
        message = ChatMessage.objects.create(
            body = body,
            author = self.user,
            chatroom = self.chatroom
        )
        # Create event dictionary
        event = {
            'type': 'message_handler',
            'message_id': message.id
        }
        # Broadcast text data to channel group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, event
        )
        
    
    # Message handler
    def message_handler(self, event):
        message_id = event['message_id']
        message = ChatMessage.objects.get(id=message_id)
        # Create context dictionary
        context = {
            'message': message,
            'author': self.user,
            'user': self.user
        }
        # Send text data to front end
        html = render_to_string("chat/partials/chat_message_partial.html", context=context)
        self.send(text_data=html)
        
        
    # Update the online count on users' screens
    def update_online_count(self):
        online_count = self.chatroom.usersOnline.count() - 1
        
        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }
        
        async_to_sync(self.channel_layer.group_send)(self.room_name, event)
        
        
    # Online count handler
    def online_count_handler(self, event):
        online_count = event['online_count']
        html = render_to_string("chat/partials/online_count_partial.html", {'online_count': online_count})
        self.send(text_data=html)