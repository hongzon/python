from django import forms

from .models import User
from django.utils.translation import gettext_lazy as _

from django.core import validators
class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput, min_length=6, max_length=20)
    # password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=20)
    email = forms.CharField(widget=forms.EmailInput, max_length=255)
    class Meta(object):
        model = User
        fields = ('username', 'password', 'email','title','birth_date')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        msg = "Must put 'help' in subject when cc'ing yourself."
        raise forms.ValidationError(
            "Did not send for 'help' in the subject despite "
            "CC'ing yourself."
        )
