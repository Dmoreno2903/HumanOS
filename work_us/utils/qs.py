from typing import Dict
from django.db.models import QuerySet
from django.http import HttpRequest
from work_us import models as wk_models


def candidates_queryset(request: HttpRequest) -> QuerySet:
    """Filter the candidates queryset based on the user's company."""
    company = request.user.get_company()
    if not company:
        return wk_models.CandidateModel.objects.none()

    # Filter candidates by the company associated with the user
    # or if vacancy in parameters, filter by vacancy
    params: Dict = request.query_params
    filters: Dict = {
        "vacancy__company": company,
    }

    if vacancy_id := params.get("vacancy"):
        filters["vacancy"] = vacancy_id

    return (
        wk_models.CandidateModel.objects.filter(**filters).distinct().order_by("stars")
    )


def work_us_queryset(request: HttpRequest) -> QuerySet:
    """Filter the vacancies queryset based on the user's company."""
    company = request.user.get_company()
    if not company:
        return wk_models.WorkUsModel.objects.none()

    return wk_models.WorkUsModel.objects.filter(company=company).distinct()
