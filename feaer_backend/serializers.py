from rest_framework import serializers
from feaer_backend.models import Category,Collection,Sex,Tag,Product,Discount
from bson import ObjectId
from bson.errors import InvalidId
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
    class Meta:
        model=Category
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False}}

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False}}

class DiscountSerializer(serializers.ModelSerializer):
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
    class Meta:
        model=Tag
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False}}

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False}}
