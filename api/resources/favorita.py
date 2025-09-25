from flask import jsonify, request
from flask_jwt_extended import get_current_user, get_jwt_identity, jwt_required
from flask_restful import Resource
from extensions import db

from api.schemas.pelicula import PeliculaListaSchema
from models.peliculas import Pelicula, PeliculaFavorita


class FavoritaResource(Resource):
    @jwt_required()
    def get(self):
        usuario = get_current_user()
        schema = PeliculaListaSchema(many=True)
        print(usuario.peliculas_favoritas)
        return jsonify(schema.dump(usuario.peliculas_favoritas))

    @jwt_required()
    def post(self):
        usuario = get_current_user()
        data = request.get_json()
        pelicula_id = data.get("id_pelicula")
        pelicula = Pelicula.query.get(pelicula_id)
        if not pelicula:
            return {"error": "Película no encontrada"}, 404
        if pelicula in usuario.peliculas_favoritas:
            return {"message": "Ya está en favoritos"}, 200

        usuario.peliculas_favoritas.append(pelicula)
        db.session.commit()
        return {"message": "Agregada a favoritos"}, 201
    
class FavoritaItemResource(Resource):
    @jwt_required()
    def delete(self, pelicula_id):
        usuario = get_current_user()
        pelicula = Pelicula.query.get(pelicula_id)
        if not pelicula or pelicula not in usuario.peliculas_favoritas:
            return {"error": "No estaba en favoritos"}, 404
        usuario.peliculas_favoritas.remove(pelicula)
        db.session.commit()
        return {"message": "Eliminada de favoritos"}, 200