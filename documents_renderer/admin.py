from django.contrib import admin
from documents_renderer import models as dr_models


@admin.register(dr_models.DocxTemplate)
class DocxTemplateAdmin(admin.ModelAdmin):
    """Admin configuration for DocxTemplate model."""
    list_display = ('name', 'file', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'file')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
