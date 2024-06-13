from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from api.models import UploadFile

class UploadFileTestCase(TestCase):
    def setUp(self):
        UploadFile.objects.create(
            title="Test Title",
            pdf_file=SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf")
        )

    def test_upload_file_title(self):
        """Tests that the title field is saved correctly."""
        upload_file = UploadFile.objects.get(title="Test Title")
        self.assertEqual(upload_file.title, "Test Title")




    def test_upload_file_pdf_file(self):
        """Tests that the pdf_file field is saved correctly."""
        upload_file = UploadFile.objects.get(title="Test Title")
        self.assertTrue(upload_file.pdf_file.name.startswith("file"))
        self.assertTrue(upload_file.pdf_file.name.endswith(".pdf"))

        

    def test_upload_file_title_auto_set(self):
        """Tests that the title is automatically set to the filename if not provided."""
        upload_file = UploadFile.objects.create(
            pdf_file=SimpleUploadedFile("file2.pdf", b"file_content", content_type="application/pdf")
        )
        self.assertEqual(upload_file.title, "file2")