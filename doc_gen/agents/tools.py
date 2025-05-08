from django.utils import timezone
from whatsapp.utils import api as whatsapp_api
from people import models as people_models
from doc_gen import models as doc_gen_models


whatsapp = whatsapp_api.WhatsAppAPI()

def send_laboral_contract(user: people_models.Person):
    """
    Get laboral contract for the user.
    """

    try:
        laboral_contract_obj = doc_gen_models.UserRequestedDoc.objects.get(
            user=user,
            doc_type=doc_gen_models.UserRequestedDoc.DocType.LABORAL_CONTRACT,
            expire_at__gt=timezone.now(),
        )

        whatsapp.send_message(
            user.phone,
            "Tu contrato laboral está disponible en el siguiente enlace: "
            f"{laboral_contract_obj.get_public_url()}.",
        )
    except doc_gen_models.UserRequestedDoc.DoesNotExist:
        whatsapp.send_message(
            user.phone,
            "No tienes un contrato laboral disponible. Por favor, contacta a tu supervisor para más información.",
        )


def send_available_vacation_days(user: people_models.Person):
    """
    Get available vacation days for the user.
    """
    try:
        days = user.get_available_vacation_days()
        whatsapp.send_message(
            user.phone,
            f"Tienes {days} días de vacaciones disponibles.",
        )
    except Exception as e:
        whatsapp.send_message(
            user.phone,
            "No pude obtener la información de tus vaciones. Intenta de nuevo más tarde o contacta con tu lider.",
        )
        print(f"Error calculating vacation days: {e}", flush=True)
