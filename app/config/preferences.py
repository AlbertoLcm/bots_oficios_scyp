from app.config import settings

DEFAULT_INFORMES_PATH_FILE = settings.BASE_DIR / "default_informes_path.txt"


DEFAULT_INSUMOS_PATH_FILE = settings.BASE_DIR / "default_insumos_path.txt"


def _folder_file(folder: str):
    if folder == "informes":
        return DEFAULT_INFORMES_PATH_FILE
    if folder == "insumos":
        return DEFAULT_INSUMOS_PATH_FILE
    raise ValueError(f"Tipo de carpeta desconocido: {folder}")


def save_default_folder_path(path: str | None, folder: str = "informes") -> None:
    if not path:
        return

    try:
        _folder_file(folder).write_text(path, encoding="utf-8")
    except OSError:
        pass


def load_default_folder_path(folder: str = "informes") -> str | None:
    try:
        path = _folder_file(folder).read_text(encoding="utf-8").strip()
    except OSError:
        return None

    return path or None
