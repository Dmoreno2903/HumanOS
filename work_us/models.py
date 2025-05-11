from django.db import models
from django_extensions.db.models import TimeStampedModel
from people import models as pple_models
from django.contrib.postgres.fields import ArrayField


class WorkUsModel(TimeStampedModel):
    """
    Vacancy model for WorkUs
    List all the vacancies for WorkUs
    """

    name = models.CharField(
        max_length=255,
        verbose_name="Name of the vacancy",
        help_text="Name of the vacancy",
    )
    description = models.TextField(
        verbose_name="Description of the vacancy",
        help_text="Description of the vacancy",
    )
    location = models.CharField(
        max_length=255,
        verbose_name="Location of the vacancy",
        help_text="Location of the vacancy",
    )
    salary = models.FloatField(
        verbose_name="Salary of the vacancy", help_text="Salary of the vacancy"
    )
    company = models.ForeignKey(
        pple_models.Company,
        on_delete=models.CASCADE,
        verbose_name="Company",
        help_text="Company that offers the vacancy",
    )
    requirements = ArrayField(
        models.CharField(max_length=255),
        verbose_name="Requirements of the vacancy",
        help_text="Requirements of the vacancy",
    )

    class Meta:
        verbose_name = "Vacante"
        verbose_name_plural = "Vacantes"

    def __str__(self):
        return self.name


class BackgroundPersonModel(TimeStampedModel):
    """
    Background person model for WorkUs
    List all the background persons for WorkUs
    """

    class OrganizationType(models.TextChoices):
        ATTORNEY = "Attorney", "Procuraduria General de la Nación"

    candidate = models.ForeignKey(
        "CandidateModel",
        on_delete=models.DO_NOTHING,
        verbose_name="Candidate",
        help_text="Candidate that has the background",
        related_name="backgrounds",
    )
    organization = models.CharField(
        max_length=255,
        choices=OrganizationType.choices,
        verbose_name="Organization of the background",
        help_text="Organization of the background",
    )

    query = models.TextField(
        verbose_name="Description of the background",
        help_text="Description of the background",
    )

    class Meta:
        verbose_name = "Antecedente"
        verbose_name_plural = "Antedecentes"

    def __str__(self):
        return f"{self.candidate.name} - {self.organization}"


class CandidateModel(TimeStampedModel):
    """
    Candidate model for WorkUs
    List all the candidates for WorkUs
    """

    number_id = models.CharField(
        max_length=255,
        verbose_name="Number ID of the candidate",
        help_text="Number ID of the candidate",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Name of the candidate",
        help_text="Name of the candidate",
    )
    email = models.EmailField(
        verbose_name="Email of the candidate", help_text="Email of the candidate"
    )
    phone = models.CharField(
        max_length=255,
        verbose_name="Phone of the candidate",
        help_text="Phone of the candidate",
    )
    resume = models.TextField(
        blank=True,
        null=True,
        verbose_name="Resume of the candidate",
        help_text="Resume of the candidate",
    )
    vacancy = models.ForeignKey(
        WorkUsModel,
        on_delete=models.DO_NOTHING,
        verbose_name="Vacancy",
        help_text="Vacancy that the candidate applied for",
        related_name="candidates",
    )
    cvv = models.FileField(
        upload_to="cvv/",
        verbose_name="CVV of the candidate",
        help_text="CVV of the candidate",
    )
    stars = models.IntegerField(
        default=0,
        verbose_name="Stars of the candidate",
        help_text="Stars of the candidate",
    )
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name="Comments of the candidate",
        help_text="Comments of the candidate",
    )

    class Meta:
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"

    def __str__(self):
        return self.name
