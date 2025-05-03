from django.contrib import admin
from .models import Role, PersonStatus, Company, Person

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    list_filter = ['name']

@admin.register(PersonStatus)
class PersonStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    list_filter = ['name']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'address']
    search_fields = ['name', 'city', 'address']
    list_filter = ['city']

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal Information', {
            'fields': [
                'first_name', 'last_name', 'date_of_birth', 'gender',
                'email', 'phone', 'address', 'city'
            ]
        }),
        ('Company Information', {
            'fields': ['status', 'role', 'company', 'start_date', 'end_date']
        }),
        ('ID Information', {
            'fields': ['national_id', 'expedition_date', 'expedition_place', 'expiration_date']
        }),
    ]
    
    list_display = ['first_name', 'last_name', 'email', 'phone', 'role', 'company', 'status']
    list_filter = ['status', 'role', 'company', 'gender', 'city']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'national_id']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']  # Assuming these fields come from TimerModel
