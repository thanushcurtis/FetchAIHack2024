from django.test import TestCase, Client
from django.urls import reverse
from api.models import UploadFile
from django.core.files.uploadedfile import SimpleUploadedFile

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse('upload')

    