import os
from marshmallow import ValidationError, validate, EXCLUDE, post_load, validates_schema
from marshmallow.fields import (
    Float, Int, Integer, List,
    String, Nested, Method, Pluck
)
from extensions import ma
from models.peliculas import Pelicula, Genero, Actor
from api.schemas.genero import GeneroSchema
from api.schemas.actor import ActorSchema
from config import Config
import re

from utils.archivos import build_url


def slugify(value: str) -> str:
    """Convierte el nombre en slug amigable para URLs."""
    value = re.sub(r'[^a-zA-Z0-9\s-]', '', value)  # quita caracteres raros
    value = re.sub(r'[\s_-]+', '-', value).strip('-')  # reemplaza espacios por "-"
    return value.lower()

class PeliculaSchema(ma.SQLAlchemyAutoSchema):
    nombre = String(required=True, validate=[validate.Length(min=5, max=150)])
    anio = Integer(required=True)
    puntuacion = Float(required=True)
    duracion = Integer(required=True)
    sinopsis = String(required=True, validate=[validate.Length(min=10)])
    slug = String(dump_only=True)

    generos = List(Int(), required=True, validate=[validate.Length(min=1)], load_only=True)
    actores = List(Int(), required=True, validate=[validate.Length(min=1)], load_only=True)

    class Meta: 
        model = Pelicula
        load_instance = False
        unknown = EXCLUDE
        exclude = ("poster", "banner")

    @post_load
    def make_slug(self, data, **kwargs):
        if "nombre" in data and "slug" not in data:
            data["slug"] = slugify(data["nombre"])
        return data
    
    @validates_schema
    def validate_unique_slug(self, data, **kwargs):
        slug_value = slugify(data['nombre'])
        existe = Pelicula.query.filter_by(slug=slug_value).first()
        if existe:
            if not data.get("id_pelicula"):
                # Si ya existe una pelicula con el mismo slug y es una pelicula nueva
                raise ValidationError(
                    f"Ya existe una película con el slug '{slug_value}'",
                    field_name="slug"
                )
            if existe.id_pelicula != data.get("id_pelicula"):
                # Si ya existe una pelicula con el mismo slug pero no es la misma pelicula
                raise ValidationError(
                    f"Ya existe una película con el slug '{slug_value}'",
                    field_name="slug"
                )

            
    
    @validates_schema
    def validate_generos_actores(self, data, **kwargs):
        errores = {}

        if data.get("generos"):
            ids = data["generos"]
            existentes = [g.id_genero for g in Genero.query.filter(Genero.id_genero.in_(ids)).all()]
            faltantes = set(ids) - set(existentes)
            if faltantes:
                errores["generos"] = [f"Géneros no encontrados: {list(faltantes)}"]

        if data.get("actores"):
            ids = data["actores"]
            existentes = [a.id_actor for a in Actor.query.filter(Actor.id_actor.in_(ids)).all()]
            faltantes = set(ids) - set(existentes)
            if faltantes:
                errores["actores"] = [f"Actores no encontrados: {list(faltantes)}"]

        if errores:
            raise ValidationError(errores)
        

class PeliculaDetalleSchema(ma.SQLAlchemyAutoSchema):
    generos = Nested(GeneroSchema, many=True, dump_only=True)
    actores = Nested(ActorSchema, many=True, dump_only=True)
    poster_url = Method("get_poster_url", dump_only=True)
    banner_url = Method("get_banner_url", dump_only=True)

    class Meta:
        model = Pelicula
        load_instance = False
        unknown = EXCLUDE
        exclude = ("poster", "banner")

    def get_poster_url(self, pelicula):
        return build_url(pelicula.poster, default_path="img/posters/default.jpg")

    def get_banner_url(self, pelicula):
        return build_url(pelicula.banner, default_path="img/banners/default.jpg")
    
class PeliculaListaSchema(ma.SQLAlchemyAutoSchema):
    poster_url = Method("get_poster_url", dump_only=True)
    generos = Pluck(GeneroSchema, "nombre", many=True, dump_only=True)

    class Meta:
        model = Pelicula
        load_instance = False
        fields = ("id_pelicula", "nombre", "anio", "poster_url", "generos")
        unknown = EXCLUDE



    def get_poster_url(self, pelicula):
        return build_url(pelicula.poster, default_path="img/posters/default.jpg")

class PeliculaCrearSchema(PeliculaSchema):
    nombre = String(required=True, validate=[validate.Length(min=5, max=150)])
    anio = Integer(required=True)
    puntuacion = Float(required=True)
    duracion = Integer(required=True)
    sinopsis = String(required=True, validate=[validate.Length(min=10)])

    generos = List(
        Int(),
        required=True,
        validate=[validate.Length(min=1)],
        load_only=True
    )
    actores = List(
        Int(),
        required=True,
        validate=[validate.Length(min=1)],
        load_only=True
    )

class PeliculaActualizarSchema(PeliculaSchema):

    nombre = String(required=False, validate=[validate.Length(min=5, max=150)])
    anio = Integer(required=False)
    puntuacion = Float(required=False)
    duracion = Integer(required=False)
    sinopsis = String(required=False, validate=[validate.Length(min=10)])

    generos = List(Int(), required=False, load_only=True)
    actores = List(Int(), required=False, load_only=True)

    @validates_schema
    def validate_unique_slug(self, data, **kwargs):
        if "nombre" in data:
            slug_value = slugify(data["nombre"])
            existe = Pelicula.query.filter_by(slug=slug_value).first()
            if existe:
                if not data.get("id_pelicula"):
                    raise ValidationError(
                        f"Ya existe una película con el slug '{slug_value}'",
                        field_name="slug"
                    )
                if existe.id_pelicula != data.get("id_pelicula"):
                    raise ValidationError(
                        f"Ya existe una película con el slug '{slug_value}'",
                        field_name="slug"
                    )