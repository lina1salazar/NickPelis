from marshmallow import validate
from marshmallow.fields import String
from extensions import ma
from models.peliculas import Genero

class GeneroSchema(ma.SQLAlchemyAutoSchema):
    nombre = String(required=True, validate=[validate.Length(min=3, max=50)])
    class Meta: 
        model = Genero
        load_instance = True