from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from auth.decorators import autorizacion_rol
from extensions import db

from api.schemas.actor import ActorSchema
from models.peliculas import Actor
from models.usuarios import UsuarioRol

class ActoresResource(Resource):
    method_decorators=[autorizacion_rol(UsuarioRol.ADMIN),jwt_required()]
    def get(self):
        actores= Actor.query.all()
        actores_schema= ActorSchema(many=True) 
        return jsonify(actores_schema.dump(actores))
    
    def post(self):
        actores_schema= ActorSchema()
        actor= actores_schema.load(request.json)
        db.session.add(actor)
        db.session.commit()
        return jsonify(msg='Actor Creado', actor= actores_schema.dump(actor))
    
class ActorResource(Resource):
    method_decorators=[autorizacion_rol(UsuarioRol.ADMIN),jwt_required()]
    def get(self, actor_id):
        actor= Actor.query.get_or_404(actor_id)
        actor_schema= ActorSchema()
        return jsonify(actor_schema.dump(actor))
    
    def delete(self, actor_id):
        actor= Actor.query.get_or_404(actor_id)
        db.session.delete(actor)
        db.session.commit()
        return jsonify(msg='Actor Eliminado')
    
    def put(self, actor_id):
        actor_schema= ActorSchema()
        actor= Actor.query.get_or_404(actor_id)
        actor=actor_schema.load(request.json, instance= actor)
        db.session.add(actor)
        db.session.commit()
        return jsonify(msg='Actor Actualizado', actor= actor_schema.dump(actor))
    
    