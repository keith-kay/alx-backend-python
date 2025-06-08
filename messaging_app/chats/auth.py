from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Optionally extend JWTAuthentication for custom logic.
    """
    pass