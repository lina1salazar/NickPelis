from flask_restful import Resource

class ActoresResource(Resource):
    def get(self):
        return {'msg': 'Hola Actores'}
    
    def post(self):
        return 'hola actores post'
    
class ActorResource(Resource):
    
    def get(self, actor_id):
        return 'hola actor' + str(actor_id)
    
    def delete(self, actor_id):
        return 'hola actor delete' + str(actor_id)
    
    def put(self, actor_id):
        return 'hola actor put' + str(actor_id)
    