from feaer_backend.models import User
from feaer_backend.serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate, login,logout
from feaer_backend.common.validateToken import validate_token
from bson import ObjectId
from datetime import datetime, timedelta

@api_view(['GET'])
@validate_token
def getAll(req):
    data = User.objects.all()
    data_serializer = UserSerializer(data,many=True)
    return Response(data_serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def create(req):
    # data_serializer = RegisterSerializer(data=req.data)
    data_serializer = UserSerializer(data=req.data)
    if data_serializer.is_valid():
        user = data_serializer.save()
        print('user aggin ',type(user))
        auth_token = AuthToken.objects.create(user=user)
        return Response(
            {
                    "User": data_serializer.data,
                    "Token": auth_token[1]
            }, status=status.HTTP_201_CREATED)
    return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def SignIn(req):
    Mail = req.data.get('Mail')
    Password = req.data.get('Password')
    
    user = authenticate(req, username=Mail, password=Password)
    if user is not None:
        login(req, user)
        auth_token = AuthToken.objects.create(user=user)
        return Response({
                "User": UserSerializer(user).data,
                "Token": auth_token[1]
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "message": "Thông tin đăng nhập không chính xác"
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def SignInAdmin(req):
    Mail = req.data.get('Mail')
    Password = req.data.get('Password')
    user = authenticate(req, username=Mail, password=Password)
    if user is not None:
        if not user.is_superuser:
            return Response({"message":'Không đủ quyền truy cập!'},status=status.HTTP_401_UNAUTHORIZED)
        login(req, user)
        auth_token = AuthToken.objects.create(user=user)
        return Response({
                "User": UserSerializer(user).data,
                "Token": auth_token[1]
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "message": "Thông tin đăng nhập không chính xác"
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def SignOut(req):
    invalidate_token(req)
    logout(req)
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deleteOne(req):
    if ('id' not in req.data):
        return Response('Missing id',status=status.HTTP_400_BAD_REQUEST)
    
    if not (ObjectId.is_valid(req.data['id'])):
        return Response('Id is not valid',status=status.HTTP_400_BAD_REQUEST)
    
    data = User.objects.filter(_id = ObjectId(req.data['id'])).delete()
    if (data[0] == 0):
        return Response('Thao tác thất bại',status=status.HTTP_200_OK)
    return Response('Thao tác thành công',status=status.HTTP_200_OK)
        

@api_view(['PUT'])
def edit(req):
    if ('id' not in req.data):
        return Response({'message': 'Missing id'},status=status.HTTP_400_BAD_REQUEST)
    
    if not (ObjectId.is_valid(req.data['id'])):
        return Response({'message': 'Id is not valid'},status=status.HTTP_400_BAD_REQUEST)
    try:
        sex_obj = User.objects.get(_id=ObjectId(req.data['id']))
    except User.DoesNotExist:
        return Response({'message': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
    data_serializer = UserSerializer(sex_obj, data=req.data, partial=True)
    if data_serializer.is_valid():
        data_serializer.save()
        return Response(data_serializer.data)
    return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@validate_token
def getUserInfo(req):
    id = req.GET.get('id')  
    print('id ne ',id)
    data = User.objects.filter(_id=ObjectId(id))
    data_serializer = UserSerializer(data,many=True)
    print('data_serializer ',data_serializer.data)
    return Response(data_serializer.data[0],status=status.HTTP_200_OK)


def invalidate_token(request):
    auth_header = request.headers.get('Authorization')
    print('auth_header ',auth_header)
    if auth_header:
        token = auth_header.split(' ')[1]
        print('auth_header token',AuthToken.objects.get(token_key=token[:8]))
        try:
            auth_token = AuthToken.objects.get(token_key=token[:8])
            auth_token.delete()
            return True
        except AuthToken.DoesNotExist:
            return False
    else:
        return False