from flask  import  Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from api.resources.pelicula import PeliculasResource, PeliculaResource
from api.resources.genero import GenerosResource, GeneroResource
from api.resources.actor import ActoresResource, ActorResource
from api.resources.comentario import ComentariosResource
from api.resources.usuario import UsuariosResource, UsuarioResource, UsuarioMeResource

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)

api.add_resource(PeliculasResource, '/peliculas')
api.add_resource(PeliculaResource, '/peliculas/<int:pelicula_id>')
api.add_resource(ComentariosResource, '/peliculas/<int:pelicula_id>/comentarios')
api.add_resource(GenerosResource, '/generos')
api.add_resource(GeneroResource, '/generos/<int:genero_id>')
api.add_resource(ActoresResource, '/actores')
api.add_resource(ActorResource, '/actores/<int:actor_id>')
api.add_resource(UsuariosResource, '/usuarios')
api.add_resource(UsuarioMeResource, '/me')
api.add_resource(UsuarioResource, '/usuarios/<int:usuario_id>')


@api_blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
