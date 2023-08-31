from django import forms
from api.databank.models import DataEntry, RelatedEntry

class DataEntryForm(forms.ModelForm):
    class Meta:
        model = DataEntry
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }

class RelatedEntryForm(forms.ModelForm):
    class Meta:
        model = RelatedEntry
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
