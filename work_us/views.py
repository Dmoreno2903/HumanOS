from rest_framework import viewsets
from work_us import models as wk_models
from work_us import serializers as wk_serializers


class WorkUsViewSet(viewsets.ModelViewSet):
    """
    Viewset for WorkUs
    List all the vacancies and candidates for WorkUs
    """

    queryset = wk_models.WorkUsModel.objects.all()
    serializer_class = wk_serializers.WorkUsSerializer


class CandidateViewSet(viewsets.ModelViewSet):
    """
    Viewset for Candidate
    List all the candidates for WorkUs
    """

    queryset = wk_models.CandidateModel.objects.all()
    serializer_class = wk_serializers.CandidateSerializer
