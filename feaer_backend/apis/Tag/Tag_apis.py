from feaer_backend.models import Tag
from feaer_backend.serializers import TagSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from bson import ObjectId
@api_view(['GET'])
def getAll(req):
    data = Tag.objects.all()
    data_serializer = TagSerializer(data,many=True)
    return Response(data_serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def create(req):
    data_serializer = TagSerializer(data=req.data)
    if data_serializer.is_valid():
        data_serializer.save()
        return Response(data_serializer.data, status=status.HTTP_201_CREATED)
    return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteOne(req):
    if ('id' not in req.data):
        return Response('Missing id',status=status.HTTP_400_BAD_REQUEST)
    
    if not (ObjectId.is_valid(req.data['id'])):
        return Response('Id is not valid',status=status.HTTP_400_BAD_REQUEST)
    
    data = Tag.objects.filter(_id = ObjectId(req.data['id'])).delete()
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
        sex_obj = Tag.objects.get(_id=ObjectId(req.data['id']))
    except Tag.DoesNotExist:
        return Response({'message': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
    data_serializer = TagSerializer(sex_obj, data=req.data, partial=True)
    if data_serializer.is_valid():
        data_serializer.save()
        return Response(data_serializer.data)
    return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

