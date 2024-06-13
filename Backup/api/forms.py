from django import forms
from .models import UploadFile

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class UploadPDFForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['pdf_file']

 
User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]