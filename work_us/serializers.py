from rest_framework import serializers
from work_us import models as wk_models
from work_us import agents as wk_agents
from work_us import utils as wk_utils


class WorkUsSerializer(serializers.ModelSerializer):
    """
    Serializer for WorkUs
    List all the vacancies and candidates for WorkUs
    """

    candidates_count = serializers.IntegerField()

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

    def validate_cvv(self, value):
        """Validate the CVV file
        Check if the file is a PDF or DOCX
        """
        ext = value.name.split(".")[-1].lower()
        if ext not in ["pdf", "docx"]:
            raise serializers.ValidationError("The CVV file must be a PDF or DOCX file")
        return value

    def create(self, validated_data):
        """Override the create method to add custom logic
        When a candidate create request is made, get using a AI agent a stars

        Step 1: Run the AI agent to extract information from the CVV and
        calculate the stars for the candidate.
        Step 2: Create the candidate with the extracted information.
        Step 3: Run the AI agent to consult the attorney page and get the information
        """
        # Save the CVV file to a temporary location and get the file path
        file_path: str = wk_utils.save_file_to_temp_storage(file=validated_data["cvv"])
        description_work: str = getattr(validated_data.get("vacancy"), "description")

        try:
            agent = wk_agents.ExtractInfoCVVAgent(
                file_path=file_path,
                description_work=description_work,
            )
            result: dict = agent.result
            print("Result of the AI agent:", result, flush=True)

            # Create the candidate with the extracted information
            validated_data.update(**result)
            candidate: wk_models.CandidateModel = super().create(
                validated_data=validated_data
            )
            print("Candidate created:", candidate, flush=True)
        except Exception as e:
            raise serializers.ValidationError(
                "Error in AI agent: {}".format(str(e))
            ) from e

        # Run the AI agent to consult the attorney page and get the information
        # This query run async, so we need to run it in a thread
        wk_agents.AttorneyOfficeAgent(
            id=candidate.pk,
        )

        # Delete the temporary file
        wk_utils.delete_temp_file(file_path=file_path)
        return candidate
