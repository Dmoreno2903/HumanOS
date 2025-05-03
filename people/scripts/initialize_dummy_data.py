from people import models as people_models
from django.contrib.auth import models as auth_models


class DummyData:
    def __init__(self):
        # ============= #
        # Company Roles #
        # ============= #
        self.ceo_role = people_models.Role.objects.create(name="CEO", description="Chief Executive Officer")
        self.accountant_role = people_models.Role.objects.create(name="Accountant", description="Responsible for financial records")
        self.backend_engineer_role = people_models.Role.objects.create(name="Backend Engineer", description="Responsible for server-side logic")
        self.frontend_engineer_role = people_models.Role.objects.create(name="Frontend Engineer", description="Responsible for client-side logic")
        self.human_resources_role = people_models.Role.objects.create(name="Human Resources", description="Responsible for employee relations")

        # ================ #
        # Company Statuses #
        # ================ #
        self.active_status = people_models.PersonStatus.objects.create(name="Active", description="Currently employed")
        self.terminated_status = people_models.PersonStatus.objects.create(name="Terminated", description="No longer employed")
        self.vacantion_status = people_models.PersonStatus.objects.create(name="Vacation", description="On vacation")
        self.sick_status = people_models.PersonStatus.objects.create(name="Sick", description="On sick leave")

        # ================= #
        # Dummy People Data #
        # ================= #

        self.company = people_models.Company.objects.create(name="HumanOS", address="645 Dream Road", city="Juniper")
        
        self.ceo_user = auth_models.User.objects.create_user(
            username="john.doe",
            email=f"john.doe@{self.company.name}.com",
            password="password123",
        )
        self.ceo = people_models.Person.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth="1980-01-01",
            email=f"john.doe@{self.company.name}.com",
            phone="1234567890",
            address="123 Main St",
            city="Springfield",
            national_id="123456789",
            expedition_date="1980-01-01",
            expedition_place="Springfield",
            expiration_date="2030-01-01",
            start_date="2020-01-01",
            #
            role=self.ceo_role,
            status=self.active_status,
            company=self.company,
            end_date=None,
            #
            user=self.ceo_user,
        )

        self.accountant_user = auth_models.User.objects.create_user(
            username="jane.smith",
            email=f"jane.smith@{self.company.name}.com",
            password="password123",
        )
        self.accountant = people_models.Person.objects.create(
            first_name="Jane",
            last_name="Smith",
            date_of_birth="1985-05-15",
            email=f"jane.smith@{self.company.name}.com",
            phone="0987654321",
            address="456 Elm St",
            city="Springfield",
            national_id="987654321",
            expedition_date="1985-05-15",
            expedition_place="Springfield",
            expiration_date="2035-05-15",
            start_date="2021-01-01",
            #
            role=self.accountant_role,
            status=self.active_status,
            company=self.company,
            end_date=None,
            #
            user=self.accountant_user,
        )
        
        self.backend_engineer_user = auth_models.User.objects.create_user(
            username="alice.johnson",
            email=f"alice.johnson@{self.company.name}.com",
            password="password123",
        )
        self.backend_engineer = people_models.Person.objects.create(
            first_name="Alice",
            last_name="Johnson",
            date_of_birth="1990-10-10",
            email=f"alice.johnson@{self.company.name}.com",
            phone="5551234567",
            address="789 Oak St",
            city="Springfield",
            national_id="555123456",
            expedition_date="1990-10-10",
            expedition_place="Springfield",
            expiration_date="2040-10-10",
            start_date="2022-01-01",
            #
            role=self.backend_engineer_role,
            status=self.active_status,
            company=self.company,
            end_date=None,
            #
            user=self.backend_engineer_user,
        )

        self.frontend_engineer_user = auth_models.User.objects.create_user(
            username="bob.brown",
            email=f"bob.brown@{self.company.name}.com",
            password="password123",
        )
        self.frontend_engineer = people_models.Person.objects.create(
            first_name="Bob",
            last_name="Brown",
            date_of_birth="1992-12-12",
            email=f"bob.brown@{self.company.name}.com",
            phone="5559876543",
            address="321 Pine St",
            city="Springfield",
            national_id="555987654",
            expedition_date="1992-12-12",
            expedition_place="Springfield",
            expiration_date="2042-12-12",
            start_date="2023-01-01",
            #
            role=self.frontend_engineer_role,
            status=self.active_status,
            company=self.company,
            end_date=None,
            #
            user=self.frontend_engineer_user,
        )

        self.human_resources_user = auth_models.User.objects.create_user(
            username="charlie.davis",
            email=f"charlie.davis@{self.company.name}.com",
            password="password123",
        )
        self.human_resources = people_models.Person.objects.create(
            first_name="Charlie",
            last_name="Davis",
            date_of_birth="1988-08-08",
            email=f"charlie.davis@{self.company.name}.com",
            phone="5556543210",
            address="654 Maple St",
            city="Springfield",
            national_id="555654321",
            expedition_date="1988-08-08",
            expedition_place="Springfield",
            expiration_date="2038-08-08",
            start_date="2024-01-01",
            #
            role=self.human_resources_role,
            status=self.active_status,
            company=self.company,
            end_date=None,
            #
            user=self.human_resources_user,
        )

        self.terminated_employee_user = auth_models.User.objects.create_user(
            username="eve.wilson",
            email=f"eve.wilson@{self.company.name}.com",
            password="password123",
            is_active=False,
        )
        self.terminated_employee = people_models.Person.objects.create(
            first_name="Eve",
            last_name="Wilson",
            date_of_birth="1982-02-02",
            email=f"eve.wilson@{self.company.name}.com",
            phone="5552468135",
            address="987 Cedar St",
            city="Springfield",
            national_id="555246813",
            expedition_date="1982-02-02",
            expedition_place="Springfield",
            expiration_date="2032-02-02",
            start_date="2019-01-01",
            #
            role=self.accountant_role,
            status=self.terminated_status,
            company=self.company,
            end_date="2023-01-01",
            #
            user=self.terminated_employee_user,
        )

        self.vacation_employee_user = auth_models.User.objects.create_user(
            username="dave.martinez",
            email=f"dave.martinez@{self.company.name}.com",
            password="password123",
        )
        self.vacation_employee = people_models.Person.objects.create(
            first_name="Dave",
            last_name="Martinez",
            date_of_birth="1995-03-03",
            email=f"dave.martinez@{self.company.name}.com",
            phone="5557531598",
            address="159 Birch St",
            city="Springfield",
            national_id="555753159",
            expedition_date="1995-03-03",
            expedition_place="Springfield",
            expiration_date="2045-03-03",
            start_date="2023-01-01",
            #
            role=self.backend_engineer_role,
            status=self.vacantion_status,
            company=self.company,
            end_date=None,
            #
            user=self.vacation_employee_user,
        )

        self.sick_employee_user = auth_models.User.objects.create_user(
            username="grace.garcia",
            email=f"grace.garcia@{self.company.name}.com",
            password="password123",
        )
        self.sick_employee = people_models.Person.objects.create(
            first_name="Grace",
            last_name="Garcia",
            date_of_birth="1993-04-04",
            email=f"grace.garcia@{self.company.name}.com",
            phone="5553692587",
            address="258 Spruce St",
            city="Springfield",
            national_id="555369258",
            expedition_date="1993-04-04",
            expedition_place="Springfield",
            expiration_date="2043-04-04",
            start_date="2023-01-01",
            #
            role=self.frontend_engineer_role,
            status=self.sick_status,
            company=self.company,
            end_date=None,
            #
            user=self.sick_employee_user,
        )

        self.dummy_people = [
            self.ceo,
            self.accountant,
            self.backend_engineer,
            self.frontend_engineer,
            self.human_resources,
            self.terminated_employee,
            self.vacation_employee,
            self.sick_employee,
        ]
