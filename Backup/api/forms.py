from django import forms
from .models import UploadFile

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class UploadPDFForm(forms.ModelForm):
    """
    This is a form for uploading PDF files.

    This form is used to handle the uploading of PDF files to the server.
    It uses the `UploadFile` model and includes only the `pdf_file` field.

    Attributes:
    Meta : class
        The meta-information for the form, specifying the model and fields to include.
    """

    class Meta:
        """
        Meta-information for the UploadPDFForm.

        Specifies the model to use for this form and the fields to include.
        """
        model = UploadFile
        fields = ['pdf_file']

 
User = get_user_model()

class RegisterForm(UserCreationForm):
    """
    This is a form for registering new users.

    This form is used to handle the registration of new users. It extends
    the Django `UserCreationForm` and includes fields for username, email,
    and passwords.

    Attributes:
    Meta : class
        The meta-information for the form, specifying the model and fields to include.
    """

    class Meta:
        """
        Meta-information for the RegisterForm.

        Specifies the model to use for this form and the fields to include.
        """
        model = User
        fields = ["username", "email", "password1", "password2"]