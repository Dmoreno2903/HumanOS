import os
import uuid
import subprocess

from docxtpl import DocxTemplate

from doc_gen import models as doc_gen


class Renderer:
    def __init__(self, docx_template: doc_gen.DocxTemplate, context: dict = None):
        self.docx_template = docx_template
        self.context = context or {}
        self.pdf_doc_path = None

    def render(self):
        """
        Render the docx template with the provided context.
        """
        temp_dir = "./media/temp/"
        os.makedirs(temp_dir, exist_ok=True)

        self.docx_rendered_path = f"{temp_dir}{str(uuid.uuid4())}.docx"

        docx = DocxTemplate(self.docx_template.file.path)
        docx.render(self.context)

        docx.save(self.docx_rendered_path)
        self.pdf_doc_path = docx_to_pdf(self.docx_rendered_path)

    def cleanup(self):
        """
        Cleanup the temporary files created during rendering.
        """
        try:
            os.remove(self.docx_rendered_path)
            os.remove(self.pdf_doc_path)
        except Exception as e:
            print(f"Error cleaning up files: {e}")


def docx_to_pdf(input_path: str):
    """Convert DOCX to PDF using LibreOffice in headless mode"""
    output_path = os.path.splitext(input_path)[0] + ".pdf"
    output_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        output_dir,
        input_path,
    ]

    try:
        process = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
        print(f"Conversion completed: {process.stdout.decode().strip()}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e.stderr.decode()}")
        return None
