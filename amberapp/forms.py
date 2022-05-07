from django import forms
from authapp.models import Profile, User


class ChangeUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'birthdate', 'avatar')
