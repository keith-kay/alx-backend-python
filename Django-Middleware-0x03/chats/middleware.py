lass RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Example: restrict access to /admin-action/ path
        protected_paths = ['/admin-action/']
        if any(request.path.startswith(path) for path in protected_paths):
            user = request.user
            # Check if user is authenticated and has 'admin' or 'moderator' role
            if not user.is_authenticated or not (getattr(user, 'role', None) in ['admin', 'moderator']):
                return HttpResponseForbidden("You do not have permission to perform this action.")
        return self.get_response(request)