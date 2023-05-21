from rest_framework import serializers
from feaer_backend.models import Category,Collection,Contact,User,Order,Sex,Tag,Product,Discount
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
    def to_internal_value(self, data):
        if isinstance(data, dict) and '_id' in data:
            return {'_id': data['_id']}

        return super().to_internal_value(data)

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
    Discount = DiscountSerializer(required=False)
    Sex = SexSerializer()
    Image = JSONListField()
    ImageDetail = JSONListField(required=False)
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

    def update(self, instance, validated_data):
        # Update the foreign key field (Sex)
        sex_id_data = validated_data.pop('Sex', None)
        if sex_id_data is not None and '_id' in sex_id_data:
            sex_id = str(sex_id_data['_id'])
            instance.Sex_id = ObjectId(sex_id)

        # Update other fields
        for attr, value in validated_data.items():
            print('attr ',attr,'- ',value)
            setattr(instance, attr, value)

        # Save the updated instance
        instance.save()

        return instance

    def create(self, validated_data):
        sex_id_data = validated_data.pop('Sex', {}).get('_id', None)
        if sex_id_data:
            sex_id = str(sex_id_data)
            validated_data['Sex_id'] = ObjectId(sex_id)

        return super().create(validated_data)

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
    class Meta:
        model=Order
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False}}
      

class ContactSerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer(required=False)
    class Meta:
        model=Contact
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False}}
