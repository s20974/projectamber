from django.db import models
from django import forms
from multiselectfield import MultiSelectField

from django.core.validators import RegexValidator

from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Product
        
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Message(models.Model):
	author = models.ForeignKey(User, related_name='author_message', on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.author.username

	def last_10_messages():
		return Message.objects.order_by('-timestamp').all()[:10]
