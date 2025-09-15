from extensions import ma
from marshmallow import validate
from marshmallow.fields import (
    Float, Pluck, String, Integer, DateTime
)
from models.peliculas import Comentario

class ComentarioSchema(ma.SQLAlchemyAutoSchema):
    contenido = String(required=True, validate=[validate.Length(min=5)])
    calificacion = Float(required=True, validate=[validate.Range(min=1, max=10)])


    id_usuario = Integer(dump_only=True)
    id_pelicula = Integer(dump_only=True)
    fecha_comentario = DateTime(dump_only=True)

    usuario = Pluck("UsuarioSchema", "nombre", dump_only=True)

    class Meta:
        model = Comentario
        include_fk = True
        load_instance = True
