from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Person, Role, PersonStatus, Company

class PersonAdmin(UserAdmin):
    # Add any customization to the admin interface
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role', 'company')
    fieldsets = UserAdmin.fieldsets + (
        ('Personal Info', {'fields': ('date_of_birth', 'phone', 'address', 'city', 'gender')}),
        ('Company Info', {'fields': ('status', 'role', 'company', 'start_date', 'end_date')}),
        ('National ID', {'fields': ('national_id', 'expedition_date', 'expedition_place', 'expiration_date')}),
    )

admin.site.register(Person, PersonAdmin)
admin.site.register(Role)
admin.site.register(PersonStatus)
admin.site.register(Company)