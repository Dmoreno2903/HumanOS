from requests import post

from django.conf import settings


class WhatsAppAPI:
    api_token=settings.WHATSAPP_API_TOKEN
    phone_id=settings.WHATSAPP_PHONE_ID
    message_url = f"https://graph.facebook.com/v22.0/{phone_id}/messages"

    def post_message(self, data, extra_headers=None):
      headers = {
          "Authorization": f"Bearer {self.api_token}"
      }

      if extra_headers:
          headers = {**headers, **extra_headers}

      data["messaging_product"] = "whatsapp"
      return post(
          url=self.message_url,
          json=data,
          headers=headers,
      )

    def send_reply(self, message, reply):
        sender = message["from"]
        message_id = message["id"]

        response = self.post_message(
            data={
                "to": sender,
                "text": {"body": reply},
                "context": {
                    "message_id": message_id
                }
            }
        )

        return self.__format_return(response)

    def send_message(self, to, message):
        response = self.post_message(
            data={
                "to": to,
                "type": "text",
                "recipient_type": "individual",
                "text": {"body": message}
            }
        )
  
        return self.__format_return(response)
    
    def send_template(self, template_name, to, parameters=[], extra_components=[]):
        components = [
            {
                "type": "body",
                "parameters": parameters
            }
        ]
        components.extend(extra_components)

        data = {
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": "es"
                },
                "components": components
            }
        }

        response = self.post_message(data=data)
        
        return self.__format_return(response)
    
    def __format_return(self, response):
        response = response.json()
        success = response.status_code == 200

        print(f"Success: {success} | Response: {response}")
        return success, response
