from django.db import models  

class UploadFile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, blank=True)
    pdf_file = models.FileField() 
    
    def save(self, *args, **kwargs):
        if not self.title:
            # Set the title to the filename without the extension
            self.title = self.pdf_file.name.rsplit('.', 1)[0]
        super(UploadFile, self).save(*args, **kwargs)

class SummariseRequest(models.Model):
    full_text = models.CharField(max_length=255)

class SummariseResponse(models.Model):
    summarised_text = models.TextField()

class DataMappingRequest(models.Model):
    raw_text = models.CharField(max_length=255)

class DataMappingResponse(models.Model):
    mapped_results = models.TextField()

class RecommedRequest(models.Model):
    tables = models.CharField(max_length=255)

class RecommendResponse(models.Model):
    redommendations = models.TextField()