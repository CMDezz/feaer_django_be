from rest_framework import serializers
from feaer_backend.models import Category,Collection,User,Order,Sex,Tag,Product,Discount
from bson import ObjectId
from bson.errors import InvalidId
import json

class ObjectIdSerializer(serializers.Field):
    def to_representation(self, value):
        if not ObjectId.is_valid(value):  # User submitted ID's might not be properly structured
            raise InvalidId
        return str(value)

    def to_internal_value(self, data):
        try:
            return ObjectId(str(data))  # Get the ID, then build an ObjectID instance using it
        except InvalidId:
            raise serializers.ValidationError(
                '`{}` is not a valid ObjectID'.format(data))
    
# class ObjectIdSerializer(serializers.Field):
#     def to_representation(self, value):
#         return str(value)

#     def to_internal_value(self, data):
#         return ObjectId(data)
    


class CategorySerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer(required=False)
    class Meta:
        model=Category
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False}}

class CollectionSerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer(required=False)
    class Meta:
        model=Collection
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False}}

class DiscountSerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer(required=False)
    class Meta:
        model=Discount
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False}}


class SexSerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer(required=False)
    class Meta:
        model=Sex
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False}}

class TagSerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer(required=False)
    class Meta:
        model=Tag
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False}
                        }
class JSONListField(serializers.ListField):
    def to_representation(self, value):
        return super().to_representation(value)

class JSONDictField(serializers.DictField):
    def to_representation(self, value):
        return super().to_representation(value)
    
class ProductSerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer(required=False)
    # Sex = ObjectIdSerializer()
    Category = serializers.SerializerMethodField()
    Collection = serializers.SerializerMethodField()
    Tag = serializers.SerializerMethodField()
    Discount = DiscountSerializer()
    Sex = SexSerializer()
    Image = JSONListField()
    ImageDetail = JSONListField()
    SizeAndStock = JSONDictField()

    def get_Category(self, obj):
        ids = obj.Category.values_list('_id', flat=True)
        return [str(id) for id in ids]
    def get_Tag(self, obj):
        serialize = TagSerializer(obj.Tag.all(), many=True)
        return serialize.data
    def get_Collection(self, obj):
        ids = obj.Collection.values_list('_id', flat=True)
        return [str(id) for id in ids]

    class Meta:
        model=Product
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False}}


class UserSerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer(required=False)
    # Order = serializers.SerializerMethodField()
    # Mail = serializers.EmailField(required=True)
    Password = serializers.CharField(write_only=True, required=True)
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['Mail'], validated_data['Password'])
        print('=====user sau khi tao ',user)
        return user

    class Meta:
        model=User
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False},'password':{'required':False}}

 

class OrderSerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer(required=False)
    Sex = UserSerializer()
    
    class Meta:
        model=Tag
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False}}
      

