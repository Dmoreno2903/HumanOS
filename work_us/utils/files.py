import os
import tempfile
from django.core.files.uploadedfile import InMemoryUploadedFile


def save_file_to_temp_storage(file: InMemoryUploadedFile) -> str:
    """
    Save a file to temporary storage and return the file path.
    """
    suffix = os.path.splitext(file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        for chunk in file.chunks():
            temp_file.write(chunk)
    return temp_file.name
