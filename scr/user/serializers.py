import random

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import serializers
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer

from scr.user.models import User, setKey, getKey


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=150, write_only=True)
    is_admin = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ("full_name", "email", "username", "phone", "password", "is_admin")

    def validate(self, attrs):
        activate_code = random.randint(100000, 999999)
        user = User(
            full_name=attrs['full_name'],
            email=attrs['email'],
            username=attrs['username'],
            is_admin=attrs['is_admin'],
            password=make_password(attrs['password']),
            is_active=True,
        )
        setKey(
            key=attrs['email'],
            value={
                "user": user,
                "activate_code": activate_code
            },
            timeout=300
        )
        subject = "Activate Your Account"
        html_content = render_to_string('activation.html', {'user': user, 'activate_code': activate_code})
        text_content = strip_tags(html_content)
        print(getKey(key=attrs['email']))

        from_email = f"ADORE TEAM <{settings.EMAIL_HOST_USER}>"
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[attrs['email']]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        return super().validate(attrs)


class CheckActivationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activate_code = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        data = getKey(key=attrs['email'])
        print(data)
        if data and data['activate_code'] == attrs['activate_code']:
            return attrs
        print(data)
        raise serializers.ValidationError(
            {"error": "Error activate code or email"}
        )


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'username', 'phone', "image", 'is_admin')


class UserCommentSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'image')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name', 'image')


class UserTgModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('tg_id', 'username', 'password')
