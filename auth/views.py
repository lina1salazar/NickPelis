from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from api.schemas.usuario import UsuarioCrearSchema, UsuarioSchema
from extensions import db, pwd_context, jwt


auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/registro',methods=["POST"])
def registrar_usuario():
    if not request.is_json:
        return jsonify({"msg": "Falta JSON en la solicitud"}), 400
    
    schema= UsuarioCrearSchema()
    usuario= schema.load(request.json) 
    db.session.add(usuario)
    db.session.commit()

    schema= UsuarioSchema()
    return jsonify(msg= "Usuario registrado con exito", usuario= schema.dump(usuario)), 201

@auth_blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400




