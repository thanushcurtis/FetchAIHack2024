from django.db import models  

class UploadFile(models.Model):
    """
    This is a model for uploading files.

    Attributes:
    user : auth.User
    title : CharField
    pdf_file : FileField
    """

    user = models.ForeignKey('auth.User', on_delete = models.CASCADE, 
                            null = True)
    title = models.CharField(max_length=255, blank=True)
    pdf_file = models.FileField() 
    
    def save(self, *args, **kwargs):
        """
        This method saves the file and sets the title
        of the file.
        """

        if not self.title:
            # Set the title to the filename without the extension
            self.title = self.pdf_file.name.rsplit('.', 1)[0]
        super(UploadFile, self).save(*args, **kwargs)

class SummariseRequest(models.Model):
    """
    This is the model for the summary request

    Attributes:
    full_text : CharField
    """

    full_text = models.CharField(max_length = 255)

class SummariseResponse(models.Model):
    """
    This is the model for the summary response

    Attributes:
    summarised_text : Textfield
    """

    summarised_text = models.TextField()

class DataMappingRequest(models.Model):
    """
    This is the model for the mapping request

    Attributes:
    full_text : CharField
    """

    raw_text = models.CharField(max_length = 255)

class DataMappingResponse(models.Model):
    """
    This is the model for the summary response

    Attributes:
    full_text : TextField
    """

    mapped_results = models.TextField()

class RecommedRequest(models.Model):
    """
    This is the model for the recommend request

    Attributes:
    full_text : CharField
    """

    tables = models.CharField(max_length = 255)

class RecommendResponse(models.Model):
    """
    This is the model for the summary response

    Attributes:
    full_text : TextField
    """

    redommendations = models.TextField()