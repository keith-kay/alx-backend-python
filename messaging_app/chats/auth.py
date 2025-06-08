from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of a conversation.
    Assumes the view has a `get_object()` method returning a Conversation or Message
    with a `participants` attribute (ManyToMany to User).
    """

    def has_object_permission(self, request, view, obj):
        # If obj is a Message, get its conversation
        conversation = getattr(obj, 'conversation', obj)
        # Check if the user is authenticated and is a participant
        return (
            request.user and
            request.user.is_authenticated and
            request.user in conversation.participants.all()
        )