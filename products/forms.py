from django import forms
from . models import *
from . fields import GroupedModelChoiceField

class ProductForm(forms.ModelForm):

    category = GroupedModelChoiceField(
        queryset=ProductsSubCategorie.objects.exclude(parent=None), 
        choices_groupby='parent'
        )

    class Meta:
        model = Product
        exclude = ("user",)
        fields =  ('name', 'price', 'category', 'description')


class JointProductForm(forms.ModelForm):

    category = GroupedModelChoiceField(
        queryset=ProductsSubCategorie.objects.exclude(parent=None), 
        choices_groupby='parent'
        )

    class Meta:
        model = JointProduct
        exclude = ("user",)
        fields =  ('name', 'price', 'category', 'description', 'partners')


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email or phone number"), max_length=254)
    

class SearchForm(forms.Form):
    data = forms.CharField(max_length = 50)
