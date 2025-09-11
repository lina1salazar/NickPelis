from flask  import  Blueprint
from flask_restful import Api
from api.resources.pelicula import PeliculasResource, PeliculaResource
from api.resources.genero import GenerosResource, GeneroResource
from api.resources.actor import ActoresResource, ActorResource

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)

api.add_resource(PeliculasResource, '/peliculas')
api.add_resource(PeliculaResource, '/peliculas/<int:pelicula_id>')
api.add_resource(GenerosResource, '/generos')
api.add_resource(GeneroResource, '/generos/<int:genero_id>')
api.add_resource(ActoresResource, '/actores')
api.add_resource(ActorResource, '/actores/<int:actor_id>')
