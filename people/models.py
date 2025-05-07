from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Company(TimeStampedModel):
    """Model to store the information of a company"""

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Company Name",
        help_text="Enter the name of the company",
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="Company Address",
        help_text="Enter the address of the company",
    )
    city = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Company City",
        help_text="Enter the city of the company",
    )
    logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True,
        verbose_name="Company Logo",
        help_text="Upload the logo of the company",
    )

    def __str__(self):
        return f"({self.pk}) {self.name}"


class Person(AbstractUser, TimeStampedModel):
    """Overwriting the default User model to add more fields."""

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date of Birth",
        help_text="Enter the date of birth",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Phone Number",
        help_text="Enter the phone number",
    )
    address = models.TextField(
        blank=True, null=True, verbose_name="Address", help_text="Enter the address"
    )
    city = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="City",
        help_text="Enter the city",
    )
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        verbose_name="Gender",
        help_text="Select the gender",
    )
    picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        verbose_name="Profile Picture",
        help_text="Upload the profile picture",
    )

    # National ID Field
    national_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        verbose_name="National ID",
        help_text="Enter the national ID",
    )
    expedition_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Expedition Date",
        help_text="Enter the expedition date",
    )
    expedition_place = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Expedition Place",
        help_text="Enter the expedition place",
    )
    expiration_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Expiration Date",
        help_text="Enter the expiration date",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_company(self):
        """Get the last company in which the person worked."""
        try:
            return self.companies.order_by("-created").first().company
        except Exception:
            return None


class Role(TimeStampedModel):
    """
    Model to store the role of a person.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class PersonCompany(TimeStampedModel):
    """
    Model to store the relationship between a person and a company.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        # TODO: Add more statuses as needed

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="companies",
        verbose_name="Person",
        help_text="Select the person",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="people",
        verbose_name="Company",
        help_text="Select the company",
    )
    role = models.ForeignKey(
        "Role",
        on_delete=models.CASCADE,
        related_name="person_companies",
        verbose_name="Role",
        help_text="Select the role",
    )
    start_date = models.DateField(
        verbose_name="Start Date", help_text="Enter the start date"
    )
    end_date = models.DateField(
        blank=True, null=True, verbose_name="End Date", help_text="Enter the end date"
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Status",
        help_text="Select the status",
    )

    def __str__(self):
        return f"{self.person} - {self.company}"
