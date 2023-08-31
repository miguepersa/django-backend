from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from api.users.models import User


class UserCreationForm(UserCreationForm):
     class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

class UserChangeForm(UserChangeForm):
      class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


