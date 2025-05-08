from people import models as pple_models
from whatsapp.utils import api as whatsapp_api
# from rest_framework import status, response
from genai.google import client as google_genai_client

class WhatsAppController:
    whatsapp_api = whatsapp_api.WhatsAppAPI()

    def __init__(self, data):
        self.data = data
        self.message_text = None
        self.phone = None
        self.message_id = None
        self.message_timestamp = None
        self.message_type = None

        try:
            entries = data.get("entry", [])
            if entries and isinstance(entries, list) and len(entries) > 0:
                changes = entries[0].get("changes", [])
                if changes and isinstance(changes, list) and len(changes) > 0:
                    value = changes[0].get("value", {})
                    messages = value.get("messages", [])
                    if messages and isinstance(messages, list) and len(messages) > 0:
                        message_data = messages[0]
                        text_obj = message_data.get("text", {})
                        if isinstance(text_obj, dict):
                            self.message_text = text_obj.get("body")

                        self.phone = message_data.get("from")
                        self.message_id = message_data.get("id")
                        self.message_timestamp = message_data.get("timestamp")
                        self.message_type = message_data.get("type")

        except Exception as e:
            print(f"Error parsing WhatsApp message data: {e}")

    def get_person(self) -> pple_models.Person:
        """
        Get the user information from the message data.
        """
        if not self.phone:
            print("No contact information found in the message data.")
            return None

        try:
            people_obj = pple_models.Person.objects.get(phone=self.phone)
        except pple_models.Person.DoesNotExist:
            print(f"User with phone {self.phone} does not exist.")
            return None

        print(f"User found: {people_obj}")
        return people_obj

    def respond_to_message(self) -> None:
        """
        Send a response message back to the user.
        """
        if not self.phone:
            print("No contact information found in the message data.")
            return

        structured_intents = google_genai_client.process_whatsapp_message_for_intents(
            self.message_text
        )

        if structured_intents.get("has_identifiable_intent"):
            response_message = structured_intents.get("response_message")
            self.whatsapp_api.send_message(self.phone, response_message)
        else:
            help_message = structured_intents.get("help_message")
            self.whatsapp_api.send_message(self.phone, help_message)
