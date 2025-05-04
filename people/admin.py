

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Company, Person, PersonCompany, Role


# Registrando el modelo Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "city")
    search_fields = ("name", "address", "city")


# Registrando el modelo Person
@admin.register(Person)
class PersonAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "email", "phone", "city")
    list_filter = ("gender", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "email", "phone")
    fieldsets = UserAdmin.fieldsets + (
        ("General", {"fields": ("birth_date", "phone", "address", "city")}),
        ("Identificatión", {"fields": ("gender", "picture", "national_id", "expedition_date", "expedition_place", "expiration_date")}),
    )


# Registrando el modelo Role
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")


# Registrando el modelo PersonCompany
@admin.register(PersonCompany)
class PersonCompanyAdmin(admin.ModelAdmin):
    list_display = ("person", "company", "role", "start_date", "end_date", "status")
    list_filter = ("status", "role", "company")
    search_fields = ("person__first_name", "person__last_name", "company__name")
    autocomplete_fields = ("person", "company", "role")
