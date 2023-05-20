import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from chat.models import Thread, ChatMessage
from bson import ObjectId
User = get_user_model()
from datetime import datetime

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        if 'room_name' in self.scope['url_route']['kwargs']:
            user = self.scope['url_route']['kwargs']['room_name']
            chat_room = f'user_chatroom_{user}'
        else:
            user =''
            chat_room = f'chat_admin'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })
    # async def websocket_connect(self, event):
    #     print('self channel name ',self.channel_name)
    #     # get the rooms the user has subscribed to
    #     # rooms = self.scope['url_route']['kwargs']['room_name']
        
    #     # # create a new group for the admin WebSocket connection
    #     # await self.channel_layer.group_add('admin', self.channel_name)
        
    #     # # add the connection to the groups for the subscribed rooms
    #     # for room in rooms:
    #     #     await self.channel_layer.group_add(room, self.channel_name)

    #     # await self.send({
    #     #     'type': 'websocket.accept'
    #     # })

    async def websocket_receive(self, event):
        print('receive', event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        sent_by_id = received_data.get('sent_by')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')

        if not msg:
            print('Error:: empty message')
            return False
        print('----start query')
        sent_by_user = await self.get_user_object(sent_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)
        print('-----end query')
        if not sent_by_user:
            print('Error:: sent by user is incorrect')
        if not send_to_user:
            print('Error:: send to user is incorrect')
        if not thread_obj:
            print('Error:: Thread id is incorrect')

        await self.create_chat_message(thread_obj, sent_by_user, msg)

        other_user_chat_room = f'user_chatroom_{send_to_id}'

        response = {
            'message': msg,
            'sent_by': str(sent_by_user._id),
            'thread_id': thread_id,
            'userInfo':{"Mail":sent_by_user.Mail,"Avatar":'','_id':str(sent_by_user.pk)},
            'chatName':sent_by_user.Mail,
            'time': str(datetime.now())
        }
        if (self.chat_room != 'chat_admin'):
            # await self.channel_layer.group_send(
            #     other_user_chat_room,
            #     {
            #         'type': 'chat_message',
            #         'text': json.dumps(response)
            #     }
            # )
            # await self.channel_layer.group_send(
            #     self.chat_room,
            #     {
            #         'type': 'chat_message',
            #         'text': json.dumps(response)
            #     }
            # )
            
            admin_response = response.copy()
            admin_response['isTotalSocket'] = True
            await self.channel_layer.group_send(
                'chat_admin',
                {
                    'type': 'chat_message',
                    'text': json.dumps(admin_response)
                }
            )
        # else:
            # await self.channel_layer.group_send(
            #     'chat_admin',
            #     {
            #         'type': 'chat_message',
            #         'text': json.dumps(response)
            #     }
            # )

        print('----- send mess end')

        # user =''
        # chat_room = f'user_chatroom_{user}'
        # response['type'] = 'noti'
        # await self.channel_layer.group_send(
        #     '',
        #     {
        #         'type': 'chat_message',
        #         'text': json.dumps(response,),
        #     }
        # )



    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def chat_message(self, event):
        # print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def get_user_object(self, user_id):
        print('----+++++')
        qs = User.objects.filter(pk=ObjectId(user_id))
        print('----+++++')
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_thread(self, thread_id):
        print('---sadkjasjd-+++++')
        qs = Thread.objects.filter(pk=ObjectId(thread_id))
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        print('---asdasdasd-+++++')
        return obj

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        ChatMessage.objects.create(thread=thread, user=user, message=msg)
