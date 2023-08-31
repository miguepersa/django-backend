from rest_framework import serializers
from api.users.models import User, Employee, Teacher
#from api.institutions.serializers import InstitutionSerializer
from django.contrib.auth.models import Group


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'role'
        )


class UserSerializer(serializers.ModelSerializer):
    # Serializer for the User model

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "last_login", "is_superuser", "is_staff",
                  "is_active", "date_joined", "created_at", "role", "teacher_profile", "employee_profile")

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get('excluded_fields', [])
        
        
        for f in exclude_fields:
            if f in fields:
                fields.pop(f)

        return fields

class UserTeacherSerializer(serializers.ModelSerializer):
    # Serializer for the User model when used in the TeacherSerializer

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'last_login'
        )


class TeacherSerializer(serializers.ModelSerializer):
    #institution = InstitutionSerializer(many=True)
    # Serializer for the Teacher model
    info = UserTeacherSerializer(source='user')
    stages = serializers.ListField(source='getStages')
    class Meta:
        model = Teacher
        fields = (
            'id',
            'info',
            'institution',
            'stages',
            'level',
            'type'
        )

    def get_fields(self):
        fields = super().get_fields()

        excluded_fields = self.context.get('excluded_fields', [])
        for field in excluded_fields:
            fields.pop(field, default=None)

        return fields


class EmployeeSerializer(serializers.ModelSerializer):
    # Serializer for the Employee model

    class Meta:
        model = Employee
        fields = '__all__'


class FileUploadSerializer(serializers.Serializer):
    # Serializer for file upload
    file = serializers.FileField()

    class Meta:
        fields = ['file']


class GroupSerializer(serializers.ModelSerializer):
    # Serializer for the Group model

    class Meta:
        model = Group
        fields = '__all__'


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            "username",
            "first_name",
            "last_name"
        )


class UserProfileSerializer(serializers.ModelSerializer):
    # Serializer for the User model when used to represent the user profile
    teacher_profile = TeacherSerializer()
    employee_profile = EmployeeSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "last_login", "is_superuser", "is_staff",
                  "is_active", "date_joined", "created_at", "role", "teacher_profile", "employee_profile")
