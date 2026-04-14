
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .forms import ChatMessageForm
from .models import ChatMessage
from django.contrib.auth.decorators import login_required


#Mozhet asinhronnym sdelatj, a? Ta ne, zachem. NET, NADO
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

        msgs = ChatMessage.objects.filter(chat=int(self.room_name)).order_by('id')
        for msg in msgs:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    "type": "chat_message",
                    "action": "history",
                    "id": msg.id, 
                    "message": msg.message_words,
                    "message_file": msg.message_file,
                    "username": msg.user.username}
            )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]
        if action == 'new_message':
            message = text_data_json["message"]
            if len(message)<1 or message is None:
                message = "Изображение"
            username = text_data_json["username"]
            message_file = text_data_json["message_file"]
            try:
                form = ChatMessageForm(data={'message_words': message, 'message_file': message_file.encode('utf-32', 'surrogatepass')})
            except:
                form = ChatMessageForm(data={'message_words': message, 'message_file': r"\x"})
            
            print(form.errors)
            print(form.is_valid())
            if form.is_valid():
                msg = form.save(self)
                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {
                        "type": "chat_message",
                        "action": "new_message",
                        "id": msg.id, 
                        "message": message,
                        "message_file": message_file, 
                        "username": username}
                )
        elif action == 'delete_message':
            message_id = text_data_json['message_id']
            try:
                message = ChatMessage.objects.get(id=message_id)
                message.delete()
                    
                async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name, {
                            "type": "delete_message",
                            "action": "delete_message",
                            "message_id": message_id
                        }
                    )
            except ChatMessage.DoesNotExist:
                print("You stupid ni")
                


    def chat_message(self, event):
        id = event["id"]
        message = event["message"]
        username = event["username"]
        message_file = event["message_file"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "action": event.get("action"),
            "message_file": message_file,
            "id": id,
            "message": message, 
            "username": username}))
    
    def delete_message(self, event):
        self.send(text_data=json.dumps({
            "action": event.get("action"),
            "action": "delete_message",
            "message_id": event["message_id"]
        }))