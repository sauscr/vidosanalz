import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class EventConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

    def new_event(self, event):
        self.send(text_data=json.dumps(event))
