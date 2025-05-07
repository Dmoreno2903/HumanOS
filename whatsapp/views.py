from django.conf import settings
from django.http import HttpResponse
from rest_framework import status, response, views

from whatsapp import serializers as whatsapp_serializers


class WebhookViewSet(views.APIView):
    """
    ViewSet for handling WhatsApp webhook events.
    """
    serializer_class = whatsapp_serializers.WhatsAppWebhookSerializer

    def get(self, request):
        """This method is used to verify the webhook from the Meta App config
        """
        mode = request.query_params.get('hub.mode')
        verify_token = request.query_params.get('hub.verify_token')
        challenge = request.query_params.get('hub.challenge')

        if mode == 'subscribe' and verify_token == settings.WHATSAPP_VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else:
            return response.Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        """This method is used to handle the incoming messages from WhatsApp
        """
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return response.Response(
                {"error": serializer.errors, "status": status.HTTP_200_OK}
            )
        
        serializer.save()
        
        return response.Response(status=status.HTTP_200_OK)
