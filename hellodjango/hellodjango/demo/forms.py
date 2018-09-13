from django import forms

from .models import User
from django.utils.translation import gettext_lazy as _
class UserForm(forms.ModelForm):
    # username = forms.CharField(widget=forms.TextInput, min_length=6, max_length=20)
    # password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=20)
    email = forms.CharField(widget=forms.EmailInput, max_length=255)
    birth_date = forms.DateField(required=False)
    class Meta(object):
        model = User
        fields = ('username', 'password', 'email','title','birth_date')
        labels = {
            'username': _('Writer'),
        }
        help_texts = {
            'username': _('Some useful help text.'),
        }
        error_messages = {
            'username': {
                'max_length': _("This writer's name is too long."),
            },
        }