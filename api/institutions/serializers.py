from rest_framework import serializers
from rest_framework.fields import empty
from api.users.serializers import TeacherSerializer, ContactsSerializer
from .models import Institution, InstitutionLevel


class InstitutionSerializer(serializers.ModelSerializer):

    # logo = serializers.SerializerMethodField('get_image_url')
    monitor = ContactsSerializer()
    teachers = TeacherSerializer(many=True, required=False)

    class Meta:
        model = Institution
        fields = '__all__'
        # if the field has already been explicitly declared on the serializer class, then the extra_kwargs option will be ignored.
        extra_kwargs = {'teachers': {'required': False, "many": True}}
        optional_fields = ('classrooms_per_level', 'students_per_classroom')

    def get_image_url(self, obj):
        request = self.context.get("request")
        image_url = obj.logo.url
        return request.build_absolute_uri(image_url)
    
    def get_fields(self):
        fields = super().get_fields()

        excluded_fields = self.context.get('excluded_fields', [])
        for field in excluded_fields:
            fields.pop(field, default=None)

        return fields


class InstitutionLevelSerializer(serializers.ModelSerializer):

    institution = serializers.CharField(source='institution.name')
    class Meta:
        model = InstitutionLevel
        fields = (
            'id',
            'institution',
            'name',
            'stage',
            'reference_level',
            'student_sections',
            'students_per_section',
            'institution_coordinator',
        )

    def get_fields(self):
        fields = super().get_fields()

        excluded_fields = self.context.get('excluded_fields', [])
        for field in excluded_fields:
            if field in fields.keys():
                fields.pop(field, default=None)

        return fields
    
    def __init__(self, instance=None, data=..., **kwargs):
        kwargs['partial'] = True
        super().__init__(instance, data, **kwargs)