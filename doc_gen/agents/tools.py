from django.utils import timezone
from whatsapp.utils import api as whatsapp_api
from people import models as people_models
from doc_gen import models as doc_gen_models
from doc_gen.utils import docx as docx_utils


whatsapp = whatsapp_api.WhatsAppAPI()


def send_laboral_contract(user: people_models.Person):
    """
    Get laboral contract for the user.
    """

    try:
        laboral_contract_obj = doc_gen_models.UserRequestedDoc.objects.get(
            user=user, doc_type=doc_gen_models.UserRequestedDoc.DocType.LABORAL_CONTRACT
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


def generate_laboral_letter(user: people_models.Person):
    """
    Generate laboral letter for the user.
    """
    current_docuement = doc_gen_models.UserRequestedDoc.objects.filter(
        user=user,
        doc_type=doc_gen_models.UserRequestedDoc.DocType.LABORAL_LETTER,
        expire_at__gt=timezone.now(),
    )

    # Si existe un documento vigente, lo enviamos y no generamos otro
    if current_docuement.exists():
        whatsapp.send_message(
            user.phone,
            (
                "Aqui tienes tu carta laboral: "
                f"{current_docuement.first().get_public_url()}"
            ),
        )
        return

    # Validamos que tengamos los datos suficientes para generar la carta
    user_company = user.get_company()
    user_person_company = user.get_person_company()
    leader = user_person_company.leader

    context = {
        "city_name": user_company.city,
        "date": timezone.now().strftime("%d/%m/%y"),
        "company_name": user_company.name,
        "leader_name": leader.get_full_name(),
        "leader_role": leader.get_person_company().role,
        "leader_national_id_expedition_place": leader.expedition_place,
        "leader_national_id": leader.national_id,
        "user_name": user.get_full_name(),
        "user_national_id": user.national_id,
        "user_start_date": user_person_company.start_date.strftime("%d/%m/%y"),
        "user_role": user_person_company.role,
        "user_salary": "${:,.2f}".format(user_person_company.salary),
    }

    missing_data = []
    for key, value in context.items():
        if not value:
            missing_data.append(key)

    laboral_letter_template = doc_gen_models.DocxTemplate.objects.filter(
        name="laboral_letter",
        file__isnull=False,
    ).first()
    if not laboral_letter_template:
        missing_data.append("laboral_letter_template")

    if missing_data:
        print(f"Missing data for laboral letter generation: {missing_data}", flush=True)
        whatsapp.send_message(
            user.phone,
            (
                "No tengo la información necesaria para generar tu carta laboral. "
                "Por favor, pídele a tu líder que complete la información necesaria."
            ),
        )
        return

    # Enviamos un mensaje al usuario para informarle que estamos generando la carta
    whatsapp.send_message(
        user.phone,
        "Estamos generando tu carta laboral. Te avisaremos cuando esté lista.",
    )

    # Generamos el documento
    renderer = docx_utils.Renderer(
        docx_template=laboral_letter_template, context=context
    )

    renderer.render()

    try:
        # Importar para gestión de archivos
        from django.core.files import File
        import os

        # Crear un archivo temporal como objeto File de Django
        with open(renderer.pdf_doc_path, "rb") as pdf_file:
            # Crear el objeto UserRequestedDoc y asociar el archivo
            laboral_letter_obj = doc_gen_models.UserRequestedDoc(
                user=user,
                doc_type=doc_gen_models.UserRequestedDoc.DocType.LABORAL_LETTER,
                expire_at=timezone.now() + timezone.timedelta(days=30),
            )

            # Guardar el archivo en el campo 'file'
            filename = os.path.basename(renderer.pdf_doc_path)
            laboral_letter_obj.file.save(filename, File(pdf_file), save=True)

        # Enviamos el documento al usuario
        whatsapp.send_message(
            user.phone,
            "Tu carta laboral está lista. Puedes descargarla aquí: "
            f"{laboral_letter_obj.get_public_url()}",
        )
    except Exception as e:
        print(f"Error al guardar el documento: {e}", flush=True)
        whatsapp.send_message(
            user.phone,
            "Hubo un problema al generar tu carta laboral. Por favor, intenta de nuevo más tarde.",
        )
    finally:
        # Limpiamos archivos temporales
        renderer.cleanup()
