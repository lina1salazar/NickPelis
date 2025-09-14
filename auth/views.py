from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from marshmallow import ValidationError

from api.schemas import usuario
from api.schemas.usuario import UsuarioCrearSchema, UsuarioSchema
from auth.helpers import agregar_token_a_lista, eliminar_tokens_de_usuario, token_existe
from config import Config
from extensions import db, pwd_context, jwt
from models.usuarios import Usuario, UsuarioRol


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

@auth_blueprint.route('/iniciar_sesion',methods=["POST"])
def iniciar_sesion():
    if not request.is_json:
        return jsonify({"msg": "Falta JSON en la solicitud"}), 400
    
    correo= request.json.get("correo")
    contrasena= request.json.get("contrasena")
    if not correo or not contrasena: 
        return jsonify({"msg": "Falta correo o constraseña"}), 400
    
    usuario= Usuario.query.filter_by(correo= correo).first()
    if not usuario or not pwd_context.verify(contrasena, usuario.contrasena):
       return jsonify({"msg": "Correo o constraseña incorrecta"}), 401

    access_token= create_access_token(identity= usuario.id_usuario)
    refresh_token= create_refresh_token(identity= usuario.id_usuario)

    agregar_token_a_lista(access_token)
    agregar_token_a_lista(refresh_token)
    
    return jsonify(access_token= access_token, refresh_token= refresh_token), 200

@auth_blueprint.route('/refrescar',methods=["POST"])
@jwt_required(refresh= True)
def refrescar():
    id_usuario= get_jwt_identity()
    access_token= create_access_token(identity= id_usuario)
    agregar_token_a_lista(access_token)
    return jsonify(access_token= access_token)

@auth_blueprint.route("/desconectar", methods=["POST"])
@jwt_required()
def desconectar():
    id_usuario = get_jwt_identity()
    eliminar_tokens_de_usuario(id_usuario)
    return {"msg": "Sesión cerrada en todos los dispositivos"}, 200


@jwt.user_lookup_loader
def buscar_usuario(_jwt_header, jwt_payload):
    identidad = jwt_payload[Config.JWT_IDENTITY_CLAIM]
    return Usuario.query.get(identidad)

@jwt.additional_claims_loader
def agregar_claims_a_token_acceso(identity):
    usuario = Usuario.query.get(identity)
    return {"rol": usuario.rol if usuario else UsuarioRol.USUARIO}

@jwt.token_in_blocklist_loader
def validar_si_token_esta_bloqueado(_jwt_header, jwt_payload):
    identificador_unico = jwt_payload["jti"]
    token = token_existe(identificador_unico)
    return token is None
    

