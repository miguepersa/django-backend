from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from api.forums.models import *
from api.users.serializers import UserSerializer


class TopicMessageReadBySerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = TopicMessageReadBy
        fields = ('id', 'user', 'date')


class ForumTopicSerializer(ModelSerializer):
    message_count = serializers.IntegerField(source='getNumberOfMessages', required=False)
    class Meta:
        model = ForumTopic
        optional_fields = ('message_count',)
        read_only_fields = ('last_interaction', )
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get('excluded_fields', [])

        for f in exclude_fields:
            if f in fields:
                fields.pop(f)

        return fields


class ForumSerializer(ModelSerializer):
    topics = ForumTopicSerializer(many=True, source='forum_topics')

    class Meta:
        model = Forum
        fields = (
            'id',
            'description',
            'course',
            'members',
            'topics',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["topics"] = sorted(response["topics"], key=lambda x: x['last_interaction'], reverse=True)
        return response

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get('excluded_fields', [])
        
        
        for f in exclude_fields:
            if f in fields:
                fields.pop(f)

        return fields
    
class TopicMessageSerializer(ModelSerializer):
    read_by = TopicMessageReadBySerializer(many=True, required=False)
    sender = UserSerializer(source='created_by', required=False)
    class Meta:
        model = TopicMessage
        optional_fields = ('read_by', 'sender')
        fields = '__all__'
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get('excluded_fields', [])
        
        
        for f in exclude_fields:
            if f in fields:
                fields.pop(f)

        return fields