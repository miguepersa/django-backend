from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from datetime import datetime
from django.core import serializers as djangoserializer

"""""
LoginSerializer is used to create a token (more specifically access & refresh tokens) 
if valid username & password are provided. Decoding the access token, we will get username & email. 

"""""


User = get_user_model()

class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        # token['user_id'] = user.id
        # token['username'] = user.username
        # token['email'] = user.email
        # token['is_staff'] = user.is_staff

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        # remove refresh from the payload
        # data.pop('refresh', None)
        # data['access'] = str(refresh.access_token)
        
        print(refresh)
        
        User = get_user_model()
        current_user = User.objects.get(username=self.user.username)

        # Add extra responses here
        data['id'] = current_user.id
        data['first_name'] = current_user.first_name
        data['last_name'] = current_user.last_name

        return data

"""
RegisterSerializer is basically used to register a user in the database.
"""

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user