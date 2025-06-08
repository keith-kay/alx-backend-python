from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_preview = serializers.CharField(source='message_body', read_only=True)
    sent_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'message_preview', 'sent_at_formatted']

    def get_sent_at_formatted(self, obj):
        return obj.sent_at.strftime('%Y-%m-%d %H:%M:%S')

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def validate(self, data):
        if 'participants' in data and len(data['participants']) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return data