from django.db import models
from common import models as common_models


class Role(common_models.TimerModel):
    """
    Model to store the role of a person.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class PersonStatus(common_models.TimerModel):
    """
    Model to store the status of a person.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Company(common_models.TimerModel):
    """
    Model to store the information of a company.
    """
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Person(common_models.TimerModel):
    """
    Model to store the information of a person.
    """

    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    # Personal Information
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)

    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)

    # Company Information
    status = models.ForeignKey(PersonStatus, on_delete=models.DO_NOTHING, related_name='people')
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, related_name='people')
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name='people')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    # National ID Field
    national_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    expedition_date = models.DateField(blank=True, null=True)
    expedition_place = models.CharField(max_length=255, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

    # Authentication Information
    user = models.OneToOneField(
        'auth.User', on_delete=models.CASCADE, blank=True, null=True, related_name='person'
    )
