import os
from flask import url_for
from config import Config

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_SIZE = 2 * 1024 * 1024  # 2MB

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


def save_file(file, carpeta, filename_base, old_file=None):
    """
    Guarda un archivo y retorna la ruta relativa.
    Si old_file viene con valor → lo elimina antes de guardar el nuevo.
    """
    folder_path = os.path.join(Config.UPLOAD_FOLDER, carpeta)
    os.makedirs(folder_path, exist_ok=True)

    # borrar el viejo si existe
    if old_file:
        delete_file(old_file)

    ext = os.path.splitext(file.filename)[1].lower()
    relative_path = f"img/{carpeta}/{filename_base}{ext}"
    full_path = os.path.join(Config.STATIC_FOLDER, relative_path)

    file.save(full_path)
    return relative_path


def delete_file(relative_path):
    """Elimina un archivo usando la ruta relativa guardada en DB."""
    if not relative_path:
        return
    full_path = os.path.join(Config.STATIC_FOLDER, relative_path)
    if os.path.exists(full_path):
        os.remove(full_path)

def build_url(relative_path, default_path=None):
    """
    Convierte la ruta relativa en URL pública.
    Si el archivo no existe, retorna la URL del default.
    """
    if relative_path:
        full_path = os.path.join(Config.STATIC_FOLDER, relative_path)
        if os.path.exists(full_path):
            return url_for("static", filename=relative_path, _external=True)

    if default_path:
        return url_for("static", filename=default_path, _external=True)

    return None