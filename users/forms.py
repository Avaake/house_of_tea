from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)
from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField()
    email = forms.CharField()
    last_name = forms.CharField()
    password1 = forms.CharField()
    username = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "email",
            "last_name",
            "password1",
            "username",
            "password2",
        )


class ProfileForm(UserChangeForm):
    image = forms.ImageField(required=False)
    first_name = forms.CharField()
    email = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()

    class Meta:
        model = User
        fields = (
            "image",
            "first_name",
            "email",
            "last_name",
            "username",
        )
