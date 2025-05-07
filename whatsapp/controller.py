from people import models as people_models
from whatsapp.utils import api as whatsapp_api
from rest_framework import status, response, views


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

    def get_person(self) -> people_models.Person:
        """
        Get the user information from the message data.
        """
        if not self.phone:
            print("No contact information found in the message data.")
            return None

        try:
            people_obj = people_models.Person.objects.get(phone=self.phone)
        except people_models.Person.DoesNotExist:
            print(f"User with phone {self.phone} does not exist.")
            return None
        
        print(f"User found: {people_obj}")
        return people_obj

    def say_hello(self):
        self.whatsapp_api.send_message(
            to=self.phone,
            message="Hello! This is a test message from the WhatsApp API."
        )

        return response.Response(status=status.HTTP_200_OK)
