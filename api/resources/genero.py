from flask_restful import Resource

class GenerosResource(Resource):
    def get(self):
        return {'msg': 'Hola Generos'}
    
    def post(self):
        return 'hola generos post'
    
class GeneroResource(Resource):
    def get(self, genero_id):
        return 'hola genero' + str(genero_id)
    
    def delete(self, genero_id):
        return 'hola genero delete' + str(genero_id)
    
    def put(self, genero_id):
        return 'hola peliculas put' + str(genero_id)