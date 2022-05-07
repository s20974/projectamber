from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    details = forms.CharField(widget=forms.Textarea, max_length = 5000)
    class Meta:
        model = Order
        fields = ["details"]
