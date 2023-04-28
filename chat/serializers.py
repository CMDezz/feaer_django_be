from rest_framework import serializers
from chat.models import Thread,ChatMessage
from bson import ObjectId
from bson.errors import InvalidId
import json
from django.contrib.auth import get_user_model

from feaer_backend.serializers import UserSerializer
User = get_user_model()

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
    
class ObjectIdField(serializers.Field):
    # data response to api
    def to_representation(self, value):
        if value is None:
            return None
        return str(value)

    # data lưu trong data base
    def to_internal_value(self, data): 
        try:
            return data
        except (TypeError, ValueError, InvalidId):
            return

class ThreadSerializer(serializers.ModelSerializer):
    _id = ObjectIdSerializer(required=False)    
    first_person =ObjectIdField()
    second_person = ObjectIdField()
    updated= serializers.DateTimeField(required=False, allow_null= True)
    timestamp= serializers.DateTimeField(required=False, allow_null=True)
    isActive= serializers.BooleanField(required=False)

    # nếu đã có 1 thread đang active với same id 1st & id 2nd -> trả về đoạn đó, không tạo mới
    def create(self, validated_data):
        first_person = validated_data['first_person']
        second_person = validated_data['second_person']
        # Check if an active thread already exists with the same first_person and second_person
        try: 
            exitin_thread = Thread.objects.get(first_person=first_person, second_person=second_person, isActive__in=[True])
            thread = exitin_thread
        except(Thread.DoesNotExist):
            # Create the new thread
            thread = Thread.objects.create(**validated_data)            

        return thread
    
    class Meta:
        model=Thread
        fields=('__all__')
        extra_kwargs = {'_id': {'required': False},"updated":{'required': False},"timestamp":{'required': False},"isActive":{'required': False}}
