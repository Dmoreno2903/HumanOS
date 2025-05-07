from django.urls import path
from whatsapp import views as whastapp_views

urlpatterns = [
    path("webhook/", whastapp_views.WebhookViewSet.as_view()),
]