from django.shortcuts import render
from .models import Room, Message, UserRoom, ReadRoomMessage
from .serializers import RoomSerializer, MessageSerializer, UserRoomSerializer
from api.permissions import CustomPermission
from api.users.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import render
from datetime import datetime

# def index(request):
#     return render(request, "chat/index.html")


# def room(request, room_name):
#     return render(request, "chat/room.html", {"room_name": room_name})


class RoomViewset(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [CustomPermission]

    def list(self, request):
        try:
            q = UserRoom.objects.filter(user=request.user)
            if q.exists():
                rooms = [{**RoomSerializer(i.room, context={'excluded_fields' : ['messages']}).data, 'unread_messages' : i.unread_messages} for i in q]
                
                return Response(rooms, status=status.HTTP_200_OK)
            
            else:
                return Response([], status=status.HTTP_200_OK)


        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            room = Room.objects.get(pk=pk)
            if (UserRoom.objects.filter(user=request.user, room=room).exists()):
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                return Response({'error' : 'not authorized'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def create(self, request):
        try:
            allowed_roles = ['academic_coordination', 'academy_coordination',
                             'directors', 'IT', 'monitoring_coordinator']
            data = request.data

            if len(data['users']) > 1 and request.user.role not in allowed_roles:
                return Response({'error' : 'not authorized to start groups'}, status=status.HTTP_401_UNAUTHORIZED)

            if len(data['users']) == 1:
                u2 = User.objects.get(pk=data['users'][0])
                ur1 = request.user.user_chatroom.all()
                ur2 = u2.user_chatroom.all()
                for i in ur1:
                    for j in ur2:
                        if i.room == j.room and len(i.room.user_chatroom.all()) == 2:
                            return Response({'message' : 'room already exists'})

            room = Room()
            if 'name' in data:
                room.name = data['name']
            room.save()


            u_room = UserRoom(user=request.user, room=room)
            u_room.save()

            for u in data['users']:
                u_room_2 = UserRoom(user=User.objects.get(pk=u), room=room)
                u_room_2.save()

            return Response({'message' : f'room created', 'id' : room.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PATCH'])
    def mark_read(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            messages = sorted(room.messages.all(), key=lambda x: x.id, reverse=True)
            ur = UserRoom.objects.get(room=room, user=request.user)

            for m in messages:
                if ReadRoomMessage.objects.filter(user_room=ur, message=m).exists():
                    break
                
                rrm = ReadRoomMessage.objects.create(
                    user_room = ur,
                    message = m,
                    read_date = datetime.now()
                    )
                
                m.read_by.append(request.user)
                
            ur.unread_messages = 0
            ur.save()

            return Response({'message' : 'success'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UserRoomViewset(ModelViewSet):
    serializer_class = UserRoomSerializer
    queryset = UserRoom.objects.all()
    permission_classes = [CustomPermission]

    def list(self, request):
        u = User.objects.filter(username=request.user)
        self.queryset = self.queryset.filter(user=u)
        return super().list(request)


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [CustomPermission]

    def create(self, request):
        try:
            data = {**request.data}
            file = None
            if 'file' in data:
                file = request.FILES.get("file")
                del data['file']

            for key in data.keys():
                data[key] = data[key][0]
            room = Room.objects.get(pk=data['room'])
            del data['room']
            nm = Message(**data, room=room, created_by=request.user, attachment=file)
            nm.save()

            ur = room.user_chatroom.all()
            for i in ur:
                if i.user == request.user:
                    continue
                
                i.unread_messages += 1
                i.save()

            return Response({'message' : 'Message created', 'message' : MessageSerializer(nm).data}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            raise e
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)