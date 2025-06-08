from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            try:
                conversation = Conversation.objects.get(conversation_id=conversation_id)
            except Conversation.DoesNotExist:
                return Message.objects.none()
            if self.request.user not in conversation.participants.all():
                return Message.objects.none()
            return Message.objects.filter(conversation=conversation)
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        if not conversation_id:
            return Response({'detail': 'conversation_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'detail': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)
        if request.user not in conversation.participants.all():
            return Response({'detail': 'Forbidden.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants')
        if not participants or len(participants) < 2:
            return Response({'detail': 'At least two participants are required.'}, status=status.HTTP_400_BAD_REQUEST)
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)