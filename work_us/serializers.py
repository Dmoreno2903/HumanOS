import tempfile
from rest_framework import serializers
from work_us import models as wk_models
from work_us.utils import files as wk_utils_files
from work_us.agents import cvv as wk_agents_cvv


class WorkUsSerializer(serializers.ModelSerializer):
    """
    Serializer for WorkUs
    List all the vacancies and candidates for WorkUs
    """

    class Meta:
        model = wk_models.WorkUsModel
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class CandidateSerializer(serializers.ModelSerializer):
    """
    Serializer for Candidate
    List all the candidates for WorkUs
    """

    class Meta:
        model = wk_models.CandidateModel
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "name": {"required": False},
            "email": {"required": False},
            "phone": {"required": False},
        }

    def create(self, validated_data):
        """Override the create method to add custom logic
        When a candidate create request is made, get using a AI agent a stars
        """
        # Using AI agent rate the candidate
        agent = wk_agents_cvv.ExtractInfoCVVAgent(
            file_path=wk_utils_files.save_file_to_temp_storage(
                file=validated_data["cvv"]
            ),
            description_work=validated_data["vacancy"].description,
        )

        response = agent.llm_analysis()
        if "error" in response:
            raise serializers.ValidationError(
                {"error": response["error"], "message": response["message"]}
            )

        # Actualizamos los datos validados con la información extraída
        validated_data.update(
            {
                "name": response["name"],
                "email": response["email"],
                "phone": response["phone"],
                "resume": response["resume"],
                "stars": response["stars"],
                "comments": response["comments"],
            }
        )

        # Usamos super().create() para crear el candidato
        return super().create(validated_data)
