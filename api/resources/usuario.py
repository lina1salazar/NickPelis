# api/resources/usuarios.py
from flask_restful import Resource
from flask import request
from flask_jwt_extended import get_current_user, jwt_required
from marshmallow import ValidationError
from extensions import db
from models.usuarios import Usuario, UsuarioRol
from api.schemas.usuario import UsuarioSchema, UsuarioCrearSchema
from auth.decorators import autorizacion_rol

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
usuario_crear_schema = UsuarioCrearSchema()

class UsuariosResource(Resource):
    method_decorators=[autorizacion_rol(UsuarioRol.ADMIN),jwt_required()]
    def get(self):
        usuarios = Usuario.query.all()
        return usuarios_schema.dump(usuarios), 200

    def post(self):
        try:
            data = usuario_crear_schema.load(request.get_json())
        except ValidationError as err:
            return {"errors": err.messages}, 400

        db.session.add(data)
        db.session.commit()
        return usuario_schema.dump(data), 201


class UsuarioResource(Resource):
    method_decorators=[autorizacion_rol(UsuarioRol.ADMIN),jwt_required()]
    def get(self, usuario_id: int):
        usuario = Usuario.query.get_or_404(usuario_id)
        return usuario_schema.dump(usuario), 200

    def put(self, usuario_id: int):
        usuario = Usuario.query.get_or_404(usuario_id)
        data = request.get_json() or {}

        usuario_actual = get_current_user()

        if usuario.id_usuario == usuario_actual.id_usuario and "rol" in data:
            if data["rol"] != UsuarioRol.ADMIN.value:
                return {"msg": "No puedes quitarte tu propio rol de administrador"}, 400

        try:
            data = usuario_schema.load(data | {"id_usuario": usuario_id}, instance=usuario, partial=True)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        db.session.commit()
        return usuario_schema.dump(usuario), 200

    def delete(self, usuario_id: int):
        usuario = Usuario.query.get_or_404(usuario_id)
        db.session.delete(usuario)
        db.session.commit()
        return {"msg": "Usuario eliminado"}, 200


class UsuarioMeResource(Resource):
    @jwt_required()
    def get(self):
        usuario = get_current_user()
        return usuario_schema.dump(usuario), 200

    @jwt_required()
    def put(self):
        usuario = get_current_user()
        data = request.get_json() or {}

        if "rol" in data:
            data.pop("rol")

        try:
            usuario = usuario_schema.load(data, instance=usuario, partial=True)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        db.session.commit()
        return usuario_schema.dump(usuario), 200
