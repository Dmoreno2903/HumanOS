from rest_framework import viewsets
from work_us import models as wk_models
from work_us import serializers as wk_serializers
from work_us.utils import qs as wk_qs


class WorkUsViewSet(viewsets.ModelViewSet):
    """
    Viewset for WorkUs
    List all the vacancies and candidates for WorkUs
    """

    permission_classes = []
    authentication_classes = []
    queryset = wk_models.WorkUsModel.objects.all()
    serializer_class = wk_serializers.WorkUsSerializer

    def get_queryset(self):
        """Override the get_queryset method to filter by company"""
        return wk_qs.work_us_queryset(request=self.request)


class CandidateViewSet(viewsets.ModelViewSet):
    """
    Viewset for Candidate
    List all the candidates for WorkUs
    """

    permission_classes = []
    authentication_classes = []
    queryset = wk_models.CandidateModel.objects.all()
    serializer_class = wk_serializers.CandidateSerializer

    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        """Override the get_queryset method to filter by company"""
        return wk_qs.candidates_queryset(request=self.request)
