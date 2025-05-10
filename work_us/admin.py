from django.contrib import admin
from work_us import models as wk_models


@admin.register(wk_models.WorkUsModel)
class WorkUsAdmin(admin.ModelAdmin):
    """
    Admin panel for WorkUs
    List all the vacancies for WorkUs
    """

    list_display = ("name", "location", "salary", "company")
    search_fields = ("name", "location", "company__name")
    list_filter = ("location", "company")
    list_per_page = 10


@admin.register(wk_models.CandidateModel)
class CandidateAdmin(admin.ModelAdmin):
    """
    Admin panel for Candidate
    List all the candidates for WorkUs
    """

    list_display = ("name", "email", "phone")
    search_fields = ("name", "email", "phone")
    list_per_page = 10


@admin.register(wk_models.BackgroundPersonModel)
class BackgroundPersonAdmin(admin.ModelAdmin):
    """
    Admin panel for BackgroundPerson
    List all the background persons for WorkUs
    """

    list_display = ("candidate", "organization", "created")
    search_fields = ("candidate__name", "organization")
    list_filter = ("organization",)
    list_per_page = 10
