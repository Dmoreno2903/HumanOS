import re
import json
from google import genai
from django.conf import settings


from genai.google.context import WHATSAPP_INTENTS_CONTEXT


client = genai.Client(api_key=settings.GEMINI_API_KEY)


DEFAULT_ERROR_RESPONSE = {
    "help_message": "Tenemos un problema y no podemos ayudarte en este momento. Por favor, intenta más tarde.",
}

def process_whatsapp_message_for_intents(message: str) -> dict:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{WHATSAPP_INTENTS_CONTEXT}\n{message}",
    )

    response_text = response.text
    json_match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL)

    if json_match:
        try:
            json_str = json_match.group(1)
            response_dict = json.loads(json_str)

            # Validate schema before returning
            if (
                "has_identifiable_intent" in response_dict
                and "intents" in response_dict
                and "help_message" in response_dict
                and "response_message" in response_dict
            ):
                return response_dict
            else:
                print(f"Invalid response schema. {response_dict}", flush=True)
                return DEFAULT_ERROR_RESPONSE
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON from response: {e}", flush=True)
            print(f"Response: {response.to_json_dict()}", flush=True)
            return DEFAULT_ERROR_RESPONSE
    else:
        print(f"Response: {response.to_json_dict()}", flush=True)
        return DEFAULT_ERROR_RESPONSE
