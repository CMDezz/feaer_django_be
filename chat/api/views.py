from chat.models import Thread,ChatMessage
from chat.serializers import ThreadSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from bson import ObjectId
from django.contrib.auth import get_user_model
from feaer_backend.common.validateToken import validate_token
User = get_user_model()
from django.db.models import Q
from django.db.models import F

# get danh sach thread active theo id
@api_view(['GET'])
def getThreads(req):
    if ('id' in req.GET):
        #lấy id của user
        id_user = req.GET['id']
        data = Thread.objects.filter(
            Q(first_person=ObjectId(id_user)) | Q(second_person=ObjectId(id_user)),
            isActive__in=[True],
        ).values(
           '_id', 'first_person', 'second_person', 'updated', 'timestamp', 'isActive'
        )
        dataValue = list(data)            
        data_serializer = ThreadSerializer(data=dataValue,many=True)
        if (data_serializer.is_valid()):
            # đổi thành custom response giống FE
            list_data = list(data_serializer.data)
            res = []
            print('list_data ',list_data)
            for dt in list_data:
                user = User.objects.get(pk=ObjectId(dt['first_person']))
                listMessage = getAllMessageFromThread(dt['_id'])
                customResponse = {}
                print('user ne ',user.Mail)
                customResponse['sessionId'] = dt['_id']
                customResponse['userInfo'] = {"Mail":user.Mail,"Avatar":'','_id':str(user.pk)}
                customResponse['chatName'] = user.Mail
                customResponse['time'] = dt['updated']
                customResponse['chatContent'] = listMessage
                res.append(customResponse)
                
            return Response(res,status=status.HTTP_200_OK)
        else: 
            print('@@@@@ failed ',data_serializer.errors)
        # return Response(data_serializer.data,status=status.HTTP_200_OK)
    return Response({"message":'Không thể thực hiện'},status=status.HTTP_400_BAD_REQUEST)


# chỉ cần truyền userId
@api_view(['POST'])
def createThreads(req):
    if ('id' in req.data):
        # lấy id của admin
        id_admin = User.objects.get(Mail='admin@gmail.com')
        # lấy id của user
        id_user = User.objects.get(pk = ObjectId(req.data['id']))
        data_coppy = req.data.copy()
        data_coppy['first_person'] = id_user
        data_coppy['second_person'] = id_admin
        print('data_coppy ',data_coppy)
        data_serializer = ThreadSerializer(data=data_coppy)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('@@@@@failed ',data_serializer.errors)
    return Response({"message":'Không thể thực hiện'},status=status.HTTP_400_BAD_REQUEST)


def getAllMessageFromThread(_id):
    if (_id):
        listMessage = list(ChatMessage.objects.filter(thread_id=ObjectId(_id)).order_by('timestamp'))
        res = []
        for mess in listMessage:
            customRes = {}
            customRes['fromAdmin'] = mess.user.pk == User.objects.get(Mail='admin@gmail.com').pk
            customRes['text'] = mess.message
            customRes['time'] = mess.timestamp
            res.append(customRes)
        return res
