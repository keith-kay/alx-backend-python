from datetime import datetime, time
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Restrict only for chat/messaging path, e.g., '/chat/' or '/messages/'
        restricted_paths = ['/chat/', '/messages/']
        if any(request.path.startswith(path) for path in restricted_paths):
            now = datetime.now().time()
            # Allow access only between 6PM (18:00) and 9PM (21:00)
            if not (time(18, 0) <= now <= time(21, 0)):
                return HttpResponseForbidden("Access to messaging is only allowed between 6PM and 9PM.")
        return self.get_response(request)