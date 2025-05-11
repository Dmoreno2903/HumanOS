import re
import os
import pymupdf
import mammoth
import json
import google.generativeai as genai
from typing import Optional
from pydantic import Field
from pydantic.dataclasses import dataclass
from django.conf import settings


@dataclass
class ExtractInfoCVVAgent:
    """
    Extract information from a CVV document and generate a response using Generative AI API.
    This class is designed to extract text from a PDF or DOCX file and generate a response using the Generative AI API.
    """

    file_path: str = Field(..., description="Path to the CVV document")
    description_work: str = Field(..., description="Description of the work")
    result: Optional[str] = Field(default=None, description="Result of the AI analysis")

    def __post_init__(self):
        """Initialize the agent and extract text from the document."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        self.result = self.llm_analysis()

    def extract_text(self, file_path: str) -> str:
        """Extract text from the document.

        Args:
            file_path (str): Path to the document file.
        """
        ext: str = os.path.splitext(file_path)[1].lower()

        # Check if the file is a PDF or DOCX
        # TODO: Add support for other file types if needed
        if ext == ".pdf":
            doc = pymupdf.open(file_path)
            return "\n".join([page.get_text() for page in doc])
        elif ext == ".docx":
            doc = mammoth.convert_to_text(open(file_path, "rb"))
            return doc.value
        else:
            raise ValueError(
                f"Unsupported file type: {ext}. Supported types are: .pdf, .docx"
            )

    def check_response(self, response_text: str) -> dict:
        """Check if the response is a valid JSON object with required fields.

        Args:
            response_text (str): The response text to check.
        """
        clean_text = re.sub(r"```json\s*|\s*```", "", response_text).strip()
        data = json.loads(clean_text)

        # Check for required fields
        required_fields = [
            "name",
            "resume",
            "stars",
            "comments",
        ]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # Check for valid 'stars' field
        if not isinstance(data["stars"], int) or not (1 <= data["stars"] <= 5):
            raise ValueError("'stars' must be an integer between 1 and 5")

        return data

    def llm_analysis(self) -> str:
        """Analyze the extracted text using the Generative AI"""
        content = self.extract_text(self.file_path)
        print(f"    🕵️‍♂️ Extracted content: {content}", flush=True)
        if not content:
            raise ValueError(
                "No content to analyze. Please extract text from a document first."
            )

        # Generate the prompt and the response format
        prompt = f"""
            Analiza la siguiente hoja de vida de un candidato para el siguiente puesto de trabajo:

            Puesto: {self.description_work}

            Devuelve **únicamente** un objeto JSON con la siguiente estructura, sin explicaciones ni texto adicional:

            {{
            "name": "nombre del candidato",
            "phone": "número de teléfono",
            "email": "correo electrónico",
            "resume": "experiencia laboral",
            "stars": "número de estrellas (1-5)",
            "comments": "comentarios sobre el candidato"
            }}

            Instrucciones:
            - El campo "stars" debe ser un número entero entre 1 y 5, según la calidad del perfil.
            - El campo "comments" debe justificar la calificación otorgada en "stars".
            - Si algún dato no se puede encontrar, usa `null` en su lugar (no dejes campos vacíos ni los omitas).
            - La respuesta debe estar en formato JSON válido.

            Texto a analizar:
            {content}
        """

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")

        # Generate a response
        response = model.generate_content(prompt)
        text = response.text.strip()
        return self.check_response(response_text=text)
