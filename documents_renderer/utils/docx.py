import os
import uuid

from docxtpl import DocxTemplate
from docx2pdf import convert as docx2pdf_convert

from documents_renderer import models as dr_models


class Renderer:
    def __init__(self, docx_template: dr_models.DocxTemplate, context: dict = None):
        self.docx_template = docx_template
        self.context = context or {}
        self.pdf_doc_path = None

    def render(self):
        """
        Render the docx template with the provided context.
        """
        temp_dir = "/media/temp/"
        os.makedirs(temp_dir, exist_ok=True)

        self.pdf_doc_path = f"{temp_dir}{str(uuid.uuid4())}.pdf"
        self.docx_rendered_path = f"{temp_dir}{str(uuid.uuid4())}.docx"

        # Implement the rendering logic here
        docx = DocxTemplate(self.docx_template.file.path)
        docx.render(self.context)

        docx.save(self.docx_rendered_path)
        docx2pdf_convert(self.docx_rendered_path, self.pdf_doc_path)

    def cleanup(self):
        """
        Cleanup the temporary files created during rendering.
        """
        try:
            os.remove(self.docx_rendered_path)
            os.remove(self.pdf_doc_path)
        except Exception as e:
            print(f"Error cleaning up files: {e}")
