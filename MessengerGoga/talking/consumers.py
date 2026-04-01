import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .forms import ChatMessageForm
from django.contrib.auth.decorators import login_required


#Mozhet asinhronnym sdelatj, a? Ta ne, zachem
#https://channels.readthedocs.io/en/latest/introduction.html

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.user = self.scope["user"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        form = ChatMessageForm(data={'message_words': message})
        if form.is_valid():
            form.save(self)
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message, "username": username}
        )

    def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "username": username}))