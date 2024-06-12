from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from api.forms import UploadPDFForm, RegisterForm
from django.contrib.auth import get_user_model

class UploadPDFFormTest(TestCase):
    def test_form_validity(self):
        form_data = {}
        file_data = {
            'pdf_file': SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf")
        }
        form = UploadPDFForm(data=form_data, files=file_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

class RegisterFormTest(TestCase):
    def test_form_validity(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalidity(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword123'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())