from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status, exceptions
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import BasicAuthentication
import datetime
from rest_framework.decorators import action


class SignUpViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        data['password'] = make_password(data['password'])
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=serializer.data.get('email'))
        refresh = RefreshToken.for_user(user)
        data = {
            "token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": serializer.data
        }
        return Response(data)

    def email_login(self, request, *args, **kwargs):
        print("--------------------------------")
        serializer = EmailLoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(email=request.data['email'].lower())
        except Exception as e:
            return Response([e.args[0]], status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        data = {
            "token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter tasks by the logged-in user
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
