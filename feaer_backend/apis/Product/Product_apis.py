from feaer_backend.models import Product,Category,Tag,Discount,Collection,Sex
from feaer_backend.serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

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
    id = req.query_params.get('id')
    if ('id' is None):
        return Response('Missing id',status=status.HTTP_400_BAD_REQUEST)
    print('id ne ',id)
    if not (ObjectId.is_valid(id)):
        return Response('Id is not valid',status=status.HTTP_400_BAD_REQUEST)
    
    data = Product.objects.filter(_id = ObjectId(id)).delete()
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
def getProductById(req):
    id = req.GET.get('id')  
    print('id ne ',id)
    data = Product.objects.filter(_id=ObjectId(id))
    data_serializer = ProductSerializer(data,many=True)
    print('data_serializer ',data_serializer.data)
    return Response(data_serializer.data[0],status=status.HTTP_200_OK)

@api_view(['GET'])
def getLatestProducts(req):
    data = Product.objects.order_by('-updatedAt')[:8]
    data_serializer = ProductSerializer(data, many=True)
    return Response(data_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getProductsByCategory(req):
    name = req.GET.get('category')
    category = Category.objects.get(Name=name).pk
    data = Product.objects.filter(Category=category)
    data_serializer = ProductSerializer(data, many=True)
    return Response(data_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getProductsByCategoryId(req):
    id = req.GET.get('id')
    data = Product.objects.filter(Category=ObjectId(id))
    data_serializer = ProductSerializer(data, many=True)
    return Response(data_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getTopSellerProducts(req):
    data = Product.objects.order_by('-TotalSold')[:8]
    data_serializer = ProductSerializer(data, many=True)
    return Response(data_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getProductsByTag(req):
    name = req.GET.get('tag')
    tag = Tag.objects.get(Name=name).pk
    data = Product.objects.filter(Tag=tag)
    data_serializer = ProductSerializer(data, many=True)
    return Response(data_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getProductsByTagId(req):
    id = req.GET.get('id')
    data = Product.objects.filter(Tag=ObjectId(id))
    print('dataa ',data)
    data_serializer = ProductSerializer(data, many=True)
    return Response(data_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getProductsByName(req):
    name = req.GET.get('keyword')
    data = Product.objects.filter(Name__icontains=name)
    data_serializer = ProductSerializer(data, many=True)
    return Response(data_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getProductsByDiscount(req):
    name = req.GET.get('discount')
    discount = Discount.objects.get(Name=name).pk
    data = Product.objects.filter(Discount=discount)
    data_serializer = ProductSerializer(data, many=True)
    return Response(data_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getProductsByCollection(req):
    name = req.GET.get('name')
    collection = Collection.objects.get(Name=name).pk
    data = Product.objects.filter(Collection=collection)
    data_serializer = ProductSerializer(data, many=True)
    return Response(data_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getProductsBySex(req):
    name = req.GET.get('sex')
    sex = Sex.objects.get(Name=name).pk
    data = Product.objects.filter(Collection=sex)
    data_serializer = ProductSerializer(data, many=True)
    return Response(data_serializer.data, status=status.HTTP_200_OK)
