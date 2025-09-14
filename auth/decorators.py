from functools import wraps

from flask import make_response
from flask_jwt_extended import get_current_user

def autorizacion_rol(rol):
    def wrapper(func):
        @wraps(func)
        def decorador(*args, **kwargs):
            usuario_actual = get_current_user()
            roles = rol if isinstance(rol, list) else [rol]
            if all(not usuario_actual.rol == r for r in roles):
                return make_response({"msg": "No autorizado"}, 401)
            return func(*args, **kwargs)
        return decorador
    return wrapper