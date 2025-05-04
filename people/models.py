from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel


class Person(AbstractUser, TimeStampedModel):
    """
    Overwriting the default User model to add more fields.
    """
    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)

    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)

    # National ID Field
    national_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    expedition_date = models.DateField(blank=True, null=True)
    expedition_place = models.CharField(max_length=255, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

    # Company information
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, blank=True, null=True, related_name='people')
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, blank=True, null=True, related_name='people')
    status = models.ForeignKey('PersonStatus', on_delete=models.SET_NULL, blank=True, null=True, related_name='people')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    # Profile picture
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    # Additional fields
    # Add any other fields you need
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Role(TimeStampedModel):
    """
    Model to store the role of a person.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class PersonStatus(TimeStampedModel):
    """
    Model to store the status of a person.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Company(TimeStampedModel):
    """
    Model to store the information of a company.
    """
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.name
