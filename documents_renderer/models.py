from django.db import models
from common import models as common_models


class DocxTemplate(common_models.TimerModel):
    """
    Model to store the path of the docx template.
    """
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='templates/docx/')
