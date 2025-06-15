import time
from django.http import HttpResponseForbidden
from collections import defaultdict

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store timestamps of messages per IP
        self.ip_message_times = defaultdict(list)
        self.MESSAGE_LIMIT = 5
        self.TIME_WINDOW = 60  # seconds

    def __call__(self, request):
        # Only apply to chat/message POST requests
        chat_paths = ['/chat/', '/messages/']
        if request.method == 'POST' and any(request.path.startswith(path) for path in chat_paths):
            ip = self.get_client_ip(request)
            now = time.time()
            # Remove timestamps older than 1 minute
            self.ip_message_times[ip] = [
                t for t in self.ip_message_times[ip] if now - t < self.TIME_WINDOW
            ]
            if len(self.ip_message_times[ip]) >= self.MESSAGE_LIMIT:
                return HttpResponseForbidden("Message rate limit exceeded. Try again later.")
            self.ip_message_times[ip].append(now)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip