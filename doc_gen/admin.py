from django.contrib import admin
from doc_gen import models as doc_models


@admin.register(doc_models.DocxTemplate)
class DocxTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "modified")
    search_fields = ("name",)
    readonly_fields = ("created", "modified")
    fieldsets = (
        (None, {"fields": ("name", "file")}),
        ("Metadata", {"classes": ("collapse",), "fields": ("created", "modified")}),
    )
