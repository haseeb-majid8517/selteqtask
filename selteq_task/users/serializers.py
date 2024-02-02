import datetime
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, Task
from rest_framework.exceptions import AuthenticationFailed

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    username = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

        extra_kwargs = {
            "password": {"write_only": True},
        }

class EmailLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email.lower(), password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        user.last_login = datetime.datetime.now()
        user.save()
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['user', 'task_name', 'created_at']
