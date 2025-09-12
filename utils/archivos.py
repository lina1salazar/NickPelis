import os
from flask import url_for
from config import Config

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_SIZE = 2 * 1024 * 1024  # 2MB


def find_image(id_recurso, carpeta):
    """Busca una imagen asociada al recurso y retorna la URL pública si existe."""
    for ext in ALLOWED_EXTENSIONS:
        path = os.path.join(Config.UPLOAD_FOLDER, carpeta, f"{id_recurso}.{ext}")
        if os.path.exists(path):
            return url_for("static", filename=f"img/{carpeta}/{id_recurso}.{ext}")
    return None


def validate_file(file, field_name):
    """Valida tipo y tamaño del archivo subido."""
    errors = {}
    if not file:
        errors[field_name] = [f"{field_name.capitalize()} es requerido"]
        return errors

    ext = os.path.splitext(file.filename)[1].lower().lstrip(".")
    if ext not in ALLOWED_EXTENSIONS:
        errors[field_name] = ["Formato no soportado, solo jpeg/png/jpg/webp"]

    if len(file.read()) > MAX_SIZE:
        errors[field_name] = ["El archivo es muy grande (max 2MB)"]

    file.seek(0)  # reset buffer
    return errors


def save_file(file, carpeta, filename_base):
    """Guarda un archivo eliminando versiones anteriores con distinta extensión."""
    folder_path = os.path.join(Config.UPLOAD_FOLDER, carpeta)
    os.makedirs(folder_path, exist_ok=True)

    ext = os.path.splitext(file.filename)[1].lower()
    file_path = os.path.join(folder_path, f"{filename_base}{ext}")

    # eliminar previas versiones
    for old_ext in ALLOWED_EXTENSIONS:
        old_path = os.path.join(folder_path, f"{filename_base}.{old_ext}")
        if os.path.exists(old_path):
            os.remove(old_path)

    file.save(file_path)
    return file_path


def delete_files(carpeta, filename_base):
    """Elimina todos los archivos relacionados a un recurso (diferentes extensiones)."""
    folder_path = os.path.join(Config.UPLOAD_FOLDER, carpeta)
    for ext in ALLOWED_EXTENSIONS:
        path = os.path.join(folder_path, f"{filename_base}.{ext}")
        if os.path.exists(path):
            os.remove(path)
