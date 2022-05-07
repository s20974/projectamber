from django.contrib.auth.backends import ModelBackend
from .models import User

from django.db.models.query_utils import Q
from django.contrib import messages

class CustomAuthenticationBackend(ModelBackend):

    def authenticate(self, request, phone_or_email=None, password=None):
        try:
            user = User.objects.get(
            Q(email=phone_or_email) | Q(phone=phone_or_email)
            )
            if user.check_password(password):            
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None