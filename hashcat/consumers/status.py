# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class StatusConsumer(WebsocketConsumer):
    def connect(self):
        self.task = self.scope['url_route']['kwargs']['task_id']
        async_to_sync(self.channel_layer.group_add)(self.task, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.task, self.channel_name)

    def send_status_update(self, event):
        status = event['status_update']
        self.send(text_data=json.dumps(status))
        
    # def receive(self, text_data):
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.task,
    #         {
    #             'type': 'send_status_update',
    #             'status_update' : text_data
    #         }
    #     )

