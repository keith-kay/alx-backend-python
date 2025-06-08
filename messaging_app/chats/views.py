from django.shortcuts import render
from .permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsParticipantOfConversation]
