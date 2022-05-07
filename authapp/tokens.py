from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import pyotp
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import User

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )

account_activation_token = TokenGenerator()

# def generate_key():
#     key = pyotp.random_base32()
#     if is_unique(key):
#         return key
#     generate_key()

# def is_unique(key):
#     try:
#         User.objects.get(phone_key=key)
#     except User.DoesNotExist:
#         return True
#     return False

# @receiver(pre_save, sender=User)
# def create_key(sender, instance, **kwargs):
#     if not instance.phone_key:
#         instance.phone_key = generate_key()