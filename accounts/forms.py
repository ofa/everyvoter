"""Forms for account app"""
from django import forms

from accounts.models import User


class UserForm(forms.Form):
    """Form for creating or modifying a user"""
    first_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    email = forms.EmailField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Email'}))


class UserEditForm(forms.ModelForm):
    """Form for users to be edited"""
    first_name = forms.CharField(
        max_length=255)
    last_name = forms.CharField(
        max_length=255)
    address = forms.CharField(
        max_length=255,
        required=False)

    class Meta(object):
        """Meta options for Form"""
        model = User
        fields = ['first_name', 'last_name', 'address']
