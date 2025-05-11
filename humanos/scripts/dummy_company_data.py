from django.utils import timezone
from people import models as people_models
from work_us import models as work_us_models


def run():
    # Create company
    company, created = people_models.Company.objects.get_or_create(
        name="HumanOS",
        defaults={
            "address": "123 Dream St",
            "city": "Dream City",
        }
    )

    # Create roles
    finance_role, created = people_models.Role.objects.get_or_create(
        name="Lider Financiero",
        defaults={
            "description": "Responsible for managing the company's finances."
        }
    )

    accountant_role, created = people_models.Role.objects.get_or_create(
        name="Contador",
        defaults={
            "description": "Responsible for managing the company's accounting."
        }
    )

    # Create users
    juanf_user, created = people_models.Person.objects.get_or_create(
        username="juanf",
        phone="3008187102",
        defaults={
            "first_name": "Juan Fernando",
            "last_name": "Cogollo",
            "email": "juan@humanos.lat",
            "birth_date": "1990-01-01",
            "address": "123 Dream St",
            "city": "Dream City",
            "gender": people_models.Person.Gender.MALE,
            "national_id": "123456789",
            "expedition_date": "2010-01-01",
            "expedition_place": "Dream City",
        }
    )

    diego_user, created = people_models.Person.objects.get_or_create(
        username="diego",
        phone="3001234567",
        defaults={
            "first_name": "Diego",
            "last_name": "Cruz",
            "email": "diego@humanos.lat",
            "birth_date": "1990-01-01",
            "address": "123 Dream St",
            "city": "Dream City",
            "gender": people_models.Person.Gender.MALE,
            "national_id": "987654321",
            "expedition_date": "2010-01-01",
            "expedition_place": "Dream City",
        }
    )

    # Create person-company relationships
    juanf_company, created = people_models.PersonCompany.objects.get_or_create(
        person=juanf_user,
        company=company,
        defaults={
            "role": accountant_role,
            "leader": diego_user,
            "start_date": "2023-01-01",
            "end_date": None,
            "salary": 10_000_000,
            "status": people_models.PersonCompany.Status.ACTIVE,
        }
    )

    diego_company, created = people_models.PersonCompany.objects.get_or_create(
        person=diego_user,
        company=company,
        defaults={
            "role": finance_role,
            "leader": None,
            "start_date": "2023-01-01",
            "end_date": None,
            "salary": 10_000_000,
            "status": people_models.PersonCompany.Status.ACTIVE,
        }
    )

    # Create vacation requests
    juanf_vacation_1, created = people_models.VacationRequest.objects.get_or_create(
        person=juanf_user,
        start_date=timezone.datetime(2023, 1, 1),
        end_date=timezone.datetime(2023, 1, 12),
        defaults={
            "status": people_models.VacationRequest.Status.APPROVED,
        }
    )

    juanf_vacation_2, created = people_models.VacationRequest.objects.get_or_create(
        person=juanf_user,
        start_date=timezone.datetime(2023, 2, 15),
        end_date=timezone.datetime(2023, 2, 21),
        defaults={
            "status": people_models.VacationRequest.Status.APPROVED,
        }
    )

    # Create work vacancy
    vacancy, created = work_us_models.WorkUsModel.objects.get_or_create(
        name="Desarrollador Backend",
        company=company,
        defaults={
            "description": "Buscamos un desarrollador backend con experiencia en Django y Python.",
            "location": "Remoto",
            "salary": 10_000_000,
            "requirements": [
                "Experiencia en Django",
                "Experiencia en Python",
                "Experiencia en bases de datos",
            ],
        }
    )