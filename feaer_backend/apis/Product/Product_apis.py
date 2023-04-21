from feaer_backend.models import Product
from feaer_backend.serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone

from bson import ObjectId
@api_view(['GET'])
def getAll(req):
    data = Product.objects.all()
    data_serializer = ProductSerializer(data,many=True)
    return Response(data_serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def create(req):
    data_serializer = ProductSerializer(data=req.data)
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
    
    data = Product.objects.filter(_id = ObjectId(req.data['id'])).delete()
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
        Product_obj = Product.objects.get(_id=ObjectId(req.data['id']))
    except Product.DoesNotExist:
        return Response({'message': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
    data_serializer = ProductSerializer(Product_obj, data=req.data, partial=True)
    if data_serializer.is_valid():
        data_serializer.save()
        return Response(data_serializer.data)
    return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getProductById(req,id):
    data = Product.objects.filter(_id=ObjectId(id))
    data_serializer = ProductSerializer(data,many=True)
    return Response(data_serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def getLatestProducts(req):
    data = Product.objects.latest(field_name=None)[:8]
    print('------------data nay ',data)
    data_serializer = ProductSerializer(data, many=True)
    return Response(data_serializer.data, status=status.HTTP_200_OK)