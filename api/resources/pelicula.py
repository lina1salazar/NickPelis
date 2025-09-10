from flask_restful import Resource

class PeliculasResource(Resource):
    def get(self):
        return {'msg': 'Hola Peliculas'}
    
    def post(self):
        return 'hola peliculas post'
    
    
    
class PeliculaResource(Resource):
    def get(self, pelicula_id):
        return 'hola pelicula' + str(pelicula_id)
    
    def delete(self, pelicula_id):
        return 'hola peliculas delete' + str(pelicula_id)
    
    def put(self, pelicula_id):
        return 'hola peliculas put' + str(pelicula_id)
