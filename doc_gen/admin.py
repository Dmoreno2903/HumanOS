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


@admin.register(doc_models.UserRequestedDoc)
class UserRequestedDocAdmin(admin.ModelAdmin):
    list_display = ("user", "doc_type", "created", "modified", "expire_at")
    list_filter = ("doc_type", "created", "expire_at")
    search_fields = ("user__first_name", "user__last_name", "doc_type")
    readonly_fields = ("created", "modified")
    fieldsets = (
        (None, {"fields": ("user", "doc_type", "file", "expire_at")}),
        ("Metadata", {"classes": ("collapse",), "fields": ("created", "modified")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")
