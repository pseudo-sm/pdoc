from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
import json, time

class Prescribe(AsyncConsumer):
    async def websocket_connect(self, event):
        self.group_name = str(self.scope['url_route']['kwargs']['slug'])
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        print('Websocket Connecting')
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_disconnect(self, event):
        print('Web Socket Disconnected')
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer

    async def websocket_receive(self, text_data):
        data = json.loads(text_data['text'])
        print("Received data:", data)  # Add a log to check the received data

        field_name = data.get('fieldName')
        field_value = data.get('value')
        print("Field Name:", field_name)  # Add a log to check the field name
        print("Field Value:", field_value)  # Add a log to check the field value
    
        if field_name == "tiny":
            print('Devidutta Sahoo')
            data_field = {
                'type': 'send.summary',
                'text': field_value
            }
            print(json.dumps(data_field))
            await self.channel_layer.group_send(
                "self.group_name", data_field
            )

    async def send_summary(self, event):
        message = event['text']
        print("Sending summary:", message)
        print("Complete message dictionary:", event)
    
        await self.send({
            'type': 'websocket.send',
            'text': message
        })