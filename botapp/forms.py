from django import forms
from .models import TelegramToken, ViberToken, Group

from django.core.validators import RegexValidator

from django.utils.translation import ugettext as _
from django.contrib.auth.password_validation import validate_password


class BaseTaskForm(forms.Form):
    task_name = forms.CharField(max_length = 100, required=True)
    telegram_tokens = forms.MultipleChoiceField()
    viber_tokens = forms.MultipleChoiceField()
    groups = forms.MultipleChoiceField()


class AddNewTelegramTokenForm(forms.Form):
    name = forms.CharField(max_length = 50 ,required = True, help_text="К чему он относится?")
    token = forms.CharField(max_length = 100, help_text="enter your token", required = True)


class AddNewViberTokenForm(forms.Form):
    name = forms.CharField(max_length = 50, required = True, help_text="К чему он относится?")
    token = forms.CharField(max_length = 100, help_text="enter your token", required = True)


class AddNewGroupForm(forms.Form):
    name = forms.CharField(max_length = 50)
    telegram_tokens = forms.MultipleChoiceField(required = False)
    viber_tokens = forms.MultipleChoiceField(required = False)
