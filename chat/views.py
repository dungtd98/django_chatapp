from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
# Create your views here.
def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


class ChatAPIView(APIView):
    def post(self, request, *args, **kwargs):
        message = request.data.get('message','')
        channel_layer = get_channel_layer()
        # channel = channel_layer.group_channels('chat_Lobby')
        async_to_sync(channel_layer.group_send)(
            'chat_Lobby',
            {
                'type':"chat_message",
                'message':message
            }
        )
        return Response({'message':message},status=status.HTTP_200_OK)

