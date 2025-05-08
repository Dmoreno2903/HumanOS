from rest_framework import serializers, status
from whatsapp import controller as whatsapp_controller


class TextSerializer(serializers.Serializer):
    body = serializers.CharField()


class DocumentSerializer(serializers.Serializer):
    filename = serializers.CharField()
    mime_type = serializers.CharField()
    sha256 = serializers.CharField()
    id = serializers.CharField()


class ButtonSerializer(serializers.Serializer):
    payload = serializers.CharField()
    text = serializers.CharField()


class ContextSerializer(serializers.Serializer):
    from_ = serializers.CharField(source="from")
    id = serializers.CharField()

    def to_internal_value(self, data):
        data["from_"] = data.pop("from", None)
        return super().to_internal_value(data)


class MessageSerializer(serializers.Serializer):
    from_ = serializers.CharField(source="from")
    id = serializers.CharField()
    timestamp = serializers.CharField()
    type = serializers.CharField()
    text = TextSerializer(required=False)
    context = ContextSerializer(required=False)
    button = ButtonSerializer(required=False)
    document = DocumentSerializer(required=False)

    def to_internal_value(self, data):
        data["from_"] = data.pop("from", None)
        return super().to_internal_value(data)


class ProfileSerializer(serializers.Serializer):
    name = serializers.CharField()


class ContactSerializer(serializers.Serializer):
    profile = ProfileSerializer()
    wa_id = serializers.CharField()


class MetadataSerializer(serializers.Serializer):
    display_phone_number = serializers.CharField()
    phone_number_id = serializers.CharField()


class ValueSerializer(serializers.Serializer):
    messaging_product = serializers.CharField()
    metadata = MetadataSerializer()
    contacts = ContactSerializer(many=True, required=False)
    messages = MessageSerializer(many=True, required=False)


class ChangeSerializer(serializers.Serializer):
    field = serializers.CharField()
    value = ValueSerializer(required=False)


class EntrySerializer(serializers.Serializer):
    id = serializers.CharField()
    changes = ChangeSerializer(many=True, required=False)


class WhatsAppWebhookSerializer(serializers.Serializer):
    object = serializers.CharField()
    entry = EntrySerializer(many=True, required=False)

    def validate(self, attrs):
        self.controller = whatsapp_controller.WhatsAppController(attrs)
        self.person_obj = self.controller.get_person()

        if not self.person_obj or not self.person_obj.is_active:
            raise serializers.ValidationError(
                {
                    "error": "User not found or inactive",
                    "status": status.HTTP_403_FORBIDDEN,
                }
            )

        return attrs

    def create(self, validated_data):
        self.controller.respond_to_message()
        return validated_data
