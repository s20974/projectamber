from django.test import TestCase

from django.contrib.auth import get_user_model
from . import models

class TestProfileModel(TestCase):
 
    @classmethod
    def test_profile_creation(self):

        User = get_user_model()
        user = User.objects.create(
            username="taskbuster", password="django-tutorial")
        self.assertIsInstance(user.profile, models.Profile)
        user.save()
        self.assertIsInstance(user.profile, models.Profile)