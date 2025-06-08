from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated participants of a conversation.
    """

    def has_permission(self, request, view):
        # Only allow access to authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # If obj is a Message, get its conversation
        conversation = getattr(obj, 'conversation', obj)
        # Only allow participants to view, send, update, or delete messages
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user in conversation.participants.all()
        return False