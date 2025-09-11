from marshmallow import validate
from marshmallow.fields import String
from extensions import ma
from models.peliculas import Actor

class ActorSchema(ma.SQLAlchemyAutoSchema): 
    nombre=String(required=True, validate=[validate.Length(min=3, max=100)])
    class Meta:
        model=Actor
        load_instance=True