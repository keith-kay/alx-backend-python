from django.urls import path, include
from rest_framework import routers
from .views import MessageViewSet, ConversationViewSet

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'conversations', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
]