import json
import openai, os
from dotenv import load_dotenv
load_dotenv('.env')
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = OPENAI_API_KEY
async def get_openai_response(prompt, model='gpt-3.5-turbo', max_tokens=1000, temperature = 0.4):
    response = openai.ChatCompletion.create(
        model = model,
        messages = [
            {'role':'user','content':prompt}
        ],
        max_tokens = max_tokens,
        temperature = temperature
    )
    return response['choices'][0]['message'].get('content', '')
async def get_openai_response_v2(prompt, model='gpt-3.5-turbo', max_tokens=1000, temperature = 0.4):
    response = openai.ChatCompletion.create(
        model = model,
        messages = [
            {'role':'user','content':prompt}
        ],
        max_tokens = max_tokens,
        temperature = temperature,
        stream = True
    )
    for chunk in response:
        content = chunk["choices"][0].get("delta", {}).get("content",'')
        yield content

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(" MESSAGE RECEIVED", text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # await self.send(text_data=json.dumps({'message':message}))
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )
        
    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        print(event)
        await self.send(text_data=json.dumps({'message':message}))
        
        # openai_response = await get_openai_response(message)
        # Send message to WebSocket
        # await self.send(text_data=json.dumps({"message": openai_response}))



