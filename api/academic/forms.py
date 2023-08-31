from django import forms
from api.academic.models import Lesson


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
        widgets = {
            'beginning': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'development': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'closure': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'achievement_indicators': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
            'main_activities': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
