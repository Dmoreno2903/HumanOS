from django.conf import settings

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


class UserRequestedDoc(ext_models.TimeStampedModel):
    """
    Model to store the user requested doc.
    """

    class DocType(models.TextChoices):
        """
        Enum for the doc types.
        """
        LABORAL_LETTER = "laboral_letter", "Carta Laboral"
        LABORAL_CONTRACT = "laboral_contract", "Contrato de Trabajo"

    def upload_to(instance, filename):
        """
        Function to upload the file to the correct path.
        """
        return f"user_docs/{instance.user.id}/{instance.user.username}_{instance.doc_type}"

    user = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        related_name="user_requested_docs",
    )

    expire_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    doc_type = models.CharField(
        max_length=50,
        choices=DocType.choices,
        default=DocType.LABORAL_LETTER,
    )

    file = models.FileField(
        upload_to=upload_to,
    )

    def get_public_url(self):
        return f"{settings.BASE_URL}{self.file.url}"
