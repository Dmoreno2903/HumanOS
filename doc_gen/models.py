from django.db import models
from django_extensions.db import models as ext_models


class DocxTemplate(ext_models.TimeStampedModel):
    """
    Model to store the docx template.
    """

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="docx_templates/")

    version = models.CharField(max_length=10, default="1.0")

    def __str__(self):
        return self.name
