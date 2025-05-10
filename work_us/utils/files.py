import os
import tempfile
from django.core.files.uploadedfile import InMemoryUploadedFile


def save_file_to_temp_storage(file: InMemoryUploadedFile) -> str:
    """
    Save a file to temporary storage and return the file path.

    Args:
        file (InMemoryUploadedFile): The file to be saved.
    """
    suffix = os.path.splitext(file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        for chunk in file.chunks():
            temp_file.write(chunk)
    return temp_file.name


def delete_temp_file(file_path: str) -> None:
    """
    Delete a temporary file.

    Args:
        file_path (str): Path to the file to be deleted.
    """
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")
    except Exception as e:
        print(f"Unexpected error deleting file {file_path}: {e}")
