from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from .models import Message, MessageSerializer

from backend.users.models import User
from backend.users.serializers import UserSerializer

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer