from rest_framework import serializers
from api.databank.models import DataEntry, RelatedEntry

class DataEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataEntry
        fields = '__all__'
        optional_fields = ('approved_by', 'approved_date')

class RelatedEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedEntry
        fields = '__all__'
        optional_fields = ('image', )
        
        