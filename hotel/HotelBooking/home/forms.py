from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AvailabilityForm(forms.Form):
    check_in=forms.DateTimeField(required=True,input_formats=['%y-%m-%dT%H:%M',])
    check_out = forms.DateTimeField(required=True, input_formats=['%y-%m-%dT%H:%M', ])
class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email']
