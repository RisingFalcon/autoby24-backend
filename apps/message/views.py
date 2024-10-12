# views.py
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message
from .serializers import MessageSerializer, CreateMessageSerializer
from .permissions import IsAdminUser, IsMessageOwner
import logging

logger = logging.getLogger(__name__)
class SendMessageView(generics.CreateAPIView):
    serializer_class = CreateMessageSerializer
    permission_classes = [IsAuthenticated]

class AdminMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_read', 'is_archived', 'is_resolved']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Message.objects.all()

class UserMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_read', 'is_archived', 'is_resolved']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageOwner]
    lookup_field = 'uuid'

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsMessageOwner | IsAdminUser]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_staff and request.user == instance.receiver:
            instance.is_read = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(is_read=True)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get_object(self):
        logger.debug(f"Attempting to retrieve message with ID: {self.kwargs.get('id')}")
        try:
            obj = super().get_object()
            logger.debug(f"Message found: {obj}")
            return obj
        except Exception as e:
            logger.error(f"Error retrieving message: {str(e)}")
            raise

class UpdateMessageStatusView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'uuid'

    def update(self, request, *args, **kwargs):
        message = self.get_object()
        status_type = request.data.get('status_type')
        if status_type == 'read':
            message.is_read = True
        elif status_type == 'archive':
            message.is_archived = True
        elif status_type == 'resolve':
            message.is_resolved = True
        message.save()
        return Response(self.get_serializer(message).data)

class AdminSendMessageView(generics.CreateAPIView):
    serializer_class = CreateMessageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context