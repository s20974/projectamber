from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile

from django.core.validators import RegexValidator

from django.utils.translation import ugettext as _
from django.contrib.auth.password_validation import validate_password


from django.forms import Textarea

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=200, required=True, label='Your name')
    last_name = forms.CharField(max_length=200, required=True, label='Your surname')
    phone_or_email = forms.CharField(max_length=200, help_text='Required', label='Phone number or email')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_or_email', 'password1', 'password2')

    def clean_password1(self):
        password = self.data.get('password1')
        validate_password(password)
        if password != self.data.get('password2'):
            raise forms.ValidationError(_("Passwords do not match"))
        return password
    
    def clean_phone_number(self):
        phone_number = self.data.get('phone_or_email')
        print(phone_number)
        if User.objects.filter(phone=phone_number).exists():
            raise forms.ValidationError(_("Another user with this phone number already exists"))
        return phone_number

class PhoneVerificationForm(forms.Form):
    one_time_password = forms.IntegerField()

    class Meta:
        fields = ('one_time_password')


class LoginForm(forms.ModelForm):
    phone_or_email = forms.CharField(max_length=200, help_text='Required', label='Phone number or email')
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('phone_or_email', 'password')
