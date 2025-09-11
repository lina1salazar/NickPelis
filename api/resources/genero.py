from flask import jsonify, request
from flask_restful import Resource
from extensions import db 

from api.schemas.genero import GeneroSchema
from models.peliculas import Genero

class GenerosResource(Resource):
    def get(self):
        generos = Genero.query.all()
        generos_schema = GeneroSchema(many = True)
        return jsonify(generos_schema.dump(generos))
    
    def post(self):
        generos_schema = GeneroSchema()
        genero = generos_schema.load(request.json)
        db.session.add(genero)
        db.session.commit()
        return jsonify(msg='Genero Creado',genero=generos_schema.dump(genero))
    
class GeneroResource(Resource):
    def get(self, genero_id):
        genero = Genero.query.get_or_404(genero_id)
        genero_schema = GeneroSchema()
        return jsonify(genero_schema.dump(genero))
    
    def put(self, genero_id):
        genero_schema = GeneroSchema()
        genero = Genero.query.get_or_404(genero_id)
        genero = genero_schema.load(request.json, instance=genero)
        db.session.add(genero)
        db.session.commit()
        return jsonify(msg='Genero Actualizado',genero=genero_schema.dump(genero))
    
    def delete(self, genero_id):
        genero = Genero.query.get_or_404(genero_id)
        db.session.delete(genero)
        db.session.commit()
        return jsonify(msg='Genero Eliminado')
    
