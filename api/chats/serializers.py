from rest_framework import serializers
from .models import *
from api.users.serializers import UserChatSerializer

class MessageSerializer(serializers.ModelSerializer):
    created_by = UserChatSerializer()
    class Meta:
        model = Message
        fields = (
            'id',
            'room',
            'message',
            'timestamp',
            'created_by',
            'status',
            'type',
            'attachment',
            )

class RoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    last_message = MessageSerializer(source='last_m')
    users = serializers.ListField(source='users_in_room')
    class Meta:
        model = Room
        read_only_fields = ('users',)
        fields = (
            'id',
            'name',
            'creation_date',
            'status',
            'messages',
            'last_message',
            'users'
        )

    def get_fields(self):
        fields = super().get_fields()

        excluded_fields = self.context.get('excluded_fields', [])
        for field in excluded_fields:
            if field in fields:
                fields.pop(field, default=None)

        return fields

class UserRoomSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    class Meta:
        model = UserRoom
        fields = '__all__'
        read_only_fields =('unread_messages', )