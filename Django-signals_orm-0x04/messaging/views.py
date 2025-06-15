from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()  # Ensure the user is deleted
        return redirect('home')  # Replace 'home' with your homepage URL name
    return

@login_required
def send_message(request):
    if request.method == "POST":
        receiver_id = request.POST.get("receiver_id")
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_message_id")
        receiver = get_object_or_404(User, pk=receiver_id)
        parent_message = None
        if parent_id:
            parent_message = get_object_or_404(Message, pk=parent_id)
        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )
        return redirect('inbox')  # Replace with your inbox view name
    users = User.objects.exclude(pk=request.user.pk)
    return render(request, "messaging/send_message.html", {"users": users})

def get_message_thread(message):
    """
    Recursively fetch all replies to a message.
    Returns a list of dicts: {'message': message, 'replies': [...]}
    """
    replies = Message.objects.filter(parent_message=message).select_related('sender', 'receiver')
    return [
        {
            'message': reply,
            'replies': get_message_thread(reply)
        }
        for reply in replies
    ]

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message.objects.select_related('sender', 'receiver'), pk=message_id)
    thread = get_message_thread(message)
    return render(request, "messaging/message_detail.html", {
        "message": message,
        "thread": thread
    })

class UnreadMessageManager(models.Manager):
    def unread_for_user(self, user):
        return self.filter(receiver=user, unread=True)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )
    unread = models.BooleanField(default=True)

    objects = models.Manager()  # Default manager
    unread = UnreadMessageManager()  # Custom manager for unread messages

@login_required
def inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user).only(
        "id", "sender", "content", "timestamp"
    )
    return render(request, "messaging/inbox.html", {"unread_messages": unread_messages})

@cache_page(60)  # Cache for 5 minutes
@login_required
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(parent_message_id=conversation_id).select_related('sender', 'receiver').order_by('timestamp')
    return render(request, "messaging/conversation_messages.html", {"messages": messages})