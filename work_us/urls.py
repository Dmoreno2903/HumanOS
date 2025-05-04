from django.urls import path, include
from rest_framework import routers
from work_us import views as wk_views

# Create a router and register our viewset with it.
router = routers.DefaultRouter()
router.register(r"vacancies", wk_views.WorkUsViewSet, basename="vacancies")
router.register(r"candidates", wk_views.CandidateViewSet, basename="candidates")

# Add the URL patterns for the API
urlpatterns = [path("", include(router.urls))]
