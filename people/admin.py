from django.contrib import admin
from django.utils.safestring import mark_safe

from django.contrib.auth.admin import UserAdmin
from .models import Company, Person, PersonCompany, Role, VacationRequest


# Registrando el modelo Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "display_logo", "city")
    search_fields = ("name", "address", "city")
    
    def display_logo(self, obj):
        if obj.logo:
            return mark_safe(f'<a href="{obj.logo.url}" target="_blank"><img src="{obj.logo.url}" style="width: 50px; height: 50px;" /></a>')
        return "-"
    
    display_logo.short_description = 'Logo'


# Registrando el modelo Person
@admin.register(Person)
class PersonAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "email", "phone", "city")
    list_filter = ("gender", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "email", "phone")
    fieldsets = UserAdmin.fieldsets + (
        ("General", {"fields": ("birth_date", "phone", "address", "city")}),
        (
            "Identificatión",
            {
                "fields": (
                    "gender",
                    "picture",
                    "national_id",
                    "expedition_date",
                    "expedition_place",
                    "expiration_date",
                )
            },
        ),
    )


# Registrando el modelo Role
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")


# Registrando el modelo PersonCompany
@admin.register(PersonCompany)
class PersonCompanyAdmin(admin.ModelAdmin):
    list_display = ("person", "company", "role", "leader", "start_date", "end_date", "status")
    list_filter = ("status", "role", "company")
    search_fields = ("person__first_name", "person__last_name", "company__name")
    autocomplete_fields = ("person", "company", "role")
    raw_id_fields = ("person", "company", "role")


# Registrando el modelo VacationRequest
@admin.register(VacationRequest)
class VacationRequestAdmin(admin.ModelAdmin):
    list_display = ("person", "start_date", "end_date", "status", "days")
    list_filter = ("status",)
    search_fields = ("person__first_name", "person__last_name")
    autocomplete_fields = ("person",)
    raw_id_fields = ("person",)
    date_hierarchy = "start_date"
    # readonly_fields = ("days",)
