from datetime import datetime
import pytz

bogota_tz = pytz.timezone("America/Bogota")

def now_bogota() -> datetime:
    """Devuelve la hora actual en zona horaria America/Bogota"""
    return datetime.now(bogota_tz)