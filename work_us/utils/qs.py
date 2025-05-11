from typing import Dict
from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest
from work_us import models as wk_models


def get_company_user(request: HttpRequest) -> str:
    """
    Get the company of the user from the request.

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        str: The company of the user.
    """
    if request.user.is_authenticated:
        return request.user.get_company()
    return None


def candidates_queryset(request: HttpRequest) -> QuerySet:
    """Filter the candidates queryset based on the user's company.

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        QuerySet: The filtered queryset of candidates.
    """
    filters: Dict = {}
    params: Dict = request.query_params

    if vacancy_id := params.get("vacancy"):
        filters["vacancy"] = vacancy_id

    company = get_company_user(request)
    if not company:
        return (
            wk_models.CandidateModel.objects.filter(**filters)
            .distinct()
            .order_by("stars")
        )

    filters["vacancy__company"] = company
    return (
        wk_models.CandidateModel.objects.filter(**filters).distinct().order_by("stars")
    )


def work_us_queryset(request: HttpRequest) -> QuerySet:
    """Filter the vacancies queryset based on the user's company.

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        QuerySet: The filtered queryset of vacancies.
    """
    company = get_company_user(request)
    if not company:
        return wk_models.WorkUsModel.objects.all().annotate(
            candidates_count=models.Count("candidates")
        )

    return wk_models.WorkUsModel.objects.filter(company=company).annotate(
        candidates_count=models.Count("candidates")
    )
