from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.databank.models import DataEntry, RelatedEntry
from api.databank.serializers import DataEntrySerializer, RelatedEntrySerializer
from api.permissions import CustomPermission
from datetime import datetime

# Create your views here.
class DataEntryViewSet(viewsets.ModelViewSet):
    serializer_class = DataEntrySerializer
    queryset = DataEntry.objects.all()
    permission_classes = [CustomPermission]

    def update(self, request, pk=None, *args, **kwargs):
        dataentry = DataEntry.objects.get(pk=pk)
        dataentry.updated_at = datetime.now()
        dataentry.updated_by = request.user
        dataentry.save()
        return super().update(request, pk, args, kwargs)
    
    @action(detail=True)
    def related(self, request, pk):
        try:
            entry = DataEntry.objects.get(pk=pk)
            pe = RelatedEntry.objects.filter(entry=entry)
            data = RelatedEntrySerializer(pe, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RelatedEntryViewSet(viewsets.ModelViewSet):
    serializer_class = RelatedEntrySerializer
    queryset = RelatedEntry.objects.all()
    permission_classes = [CustomPermission]
