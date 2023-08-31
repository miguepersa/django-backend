from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.forums.models import *
from api.forums.serializers import *
from api.permissions import CustomPermission

# Create your views here.


class ForumViewSet(ModelViewSet):
    serializer_class = ForumSerializer
    queryset = Forum.objects.all()
    permission_classes = [CustomPermission]

    def retrieve(self, request, pk, **kwargs):
        try:
            forum = Forum.objects.get(pk=pk)

            context = {
                'excluded_fields' : [
                    'topics'
                ]
            }
            
            data = ForumSerializer(forum, context=context).data
            data['topics'] = []

            topics = forum.forum_topics.all()
            for topic in topics:
                d = ForumTopicSerializer(topic).data
                d['unread_messages'] = False
                if topic.getNumberOfMessages() > len(TopicMessageReadBy.objects.filter(user=request.user, message__topic=topic)):
                    d['unread_messages'] = True

                data['topics'].append(d)

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ForumTopicViewSet(ModelViewSet):
    serializer_class = ForumTopicSerializer
    queryset = ForumTopic.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            topic_serializer = ForumTopicSerializer(data=request.data)
            if topic_serializer.is_valid(raise_exception=True):
                topic = ForumTopic(**topic_serializer.validated_data)
                if topic.forum:
                    topic.end_date = topic.forum.course.end_date
                topic.save()
                return Response({"message": "Forum topic created"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, *args, **kwargs):
        try:
            ft = ForumTopic.objects.get(pk=pk)
            for message in ft.topic_messages.all():
                if not TopicMessageReadBy.objects.filter(message=message, user=request.user).exists():
                    tm = TopicMessageReadBy(message=message, user=request.user)
                    tm.save()

            return super().partial_update(request, pk, *args, **kwargs)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk):
        try:
            topic = ForumTopic.objects.get(pk=pk)
            messages = topic.topic_messages.all()

            context = {
                'excluded_fields': [
                    "username",
                    "email",
                    "last_login",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "date_joined",
                    "created_at",
                    "role",
                    "teacher_profile",
                    "employee_profile",
                    "created_by"
                ]
            }

            data = TopicMessageSerializer(
                messages, many=True, context=context).data

            return Response(sorted(data, key=lambda x: x['date']), status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def mark_read(self, request, pk):
        try:
            topic = ForumTopic.objects.get(pk=pk)
            messages = sorted(list(topic.topic_messages.all()), key= lambda x:x.id, reverse=True)
            for i in messages:
                if i.read_by.filter(user=request.user).exists():
                    break

                rb = TopicMessageReadBy(message=i, user=request.user)
                rb.save()

            return Response({'message': 'messages marked read'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TopicMessageReadByViewSet(ModelViewSet):
    serializer_class = TopicMessageReadBySerializer
    queryset = TopicMessageReadBy.objects.all()
    permission_classes = [CustomPermission]


class TopicMessageViewSet(ModelViewSet):
    serializer_class = TopicMessageSerializer
    queryset = TopicMessage.objects.all()
    permission_classes = [CustomPermission]

    def list(self, request, *args, **kwargs):
        try:
            context = {
                'excluded_fields': [
                    "username",
                    "email",
                    "last_login",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "date_joined",
                    "created_at",
                    "role",
                    "teacher_profile",
                    "employee_profile",
                    "created_by"
                ]
            }

            data = self.serializer_class(
                self.queryset, many=True, context=context).data

            return Response(sorted(data, key=lambda x: x['date'], reverse=True), status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            data = {}
            new_data = {**request.data}
            
            for key in new_data:
                data[key] = new_data[key][0]

            attachment = request.FILES.get("attachment")
            data['attachment'] = attachment
            data['topic'] = ForumTopic.objects.get(pk=int(data['topic']))
            

            message = TopicMessage(**data)
            message.created_by = request.user
            message.save()
            topic = message.topic
            topic.last_interaction = message.date
            topic.save()
            read_by = TopicMessageReadBy(message=message, user=request.user, date=message.date)
            read_by.save()
            return Response({'message' : f'message {message.id} created'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
