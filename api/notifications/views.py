from django.shortcuts import render
from rest_framework import viewsets
from api.notifications.models import Notification
from api.notifications.serializers import NotificationSerializer
from api.permissions import CustomPermission
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [CustomPermission]

    def list(self, request):
        try:
            notifications = Notification.objects.filter(user=request.user)
            data = NotificationSerializer(notifications, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)