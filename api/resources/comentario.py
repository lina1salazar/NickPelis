from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_current_user
from marshmallow import ValidationError
from extensions import db
from models.peliculas import Comentario
from api.schemas.comentario import ComentarioSchema

class ComentariosResource(Resource):
    @jwt_required()
    def post(self, pelicula_id: int):
        schema = ComentarioSchema()
        try:
            comentario = schema.load(request.get_json())
        except ValidationError as err:
            return {"errors": err.messages}, 400

        usuario = get_current_user()

        comentario.id_pelicula = pelicula_id
        comentario.usuario = usuario

        db.session.add(comentario)
        db.session.commit()

        return {
            "msg": "Comentario Creado",
            "comentario": schema.dump(comentario)
        }, 201

    def get(self, pelicula_id: int):
        comentarios = Comentario.query.filter_by(id_pelicula=pelicula_id).all()
        schema = ComentarioSchema(many=True)
        return schema.dump(comentarios), 200
