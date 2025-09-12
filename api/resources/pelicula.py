import os
from flask import jsonify, request
from flask_restful import Resource
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload
from extensions import db

from api.schemas.pelicula import PeliculaSchema, PeliculaDetalleSchema, PeliculaListaSchema, slugify
from models.peliculas import Pelicula, Genero, Actor
from utils.archivos import delete_file, save_file, validate_file

  
class PeliculasResource(Resource):
    def get(self):

        query = Pelicula.query.options(joinedload(Pelicula.generos))

        # Búsqueda por texto
        search = request.args.get("q")
        if search:
            like = f"%{search.lower()}%"
            query = query.filter(
                (Pelicula.nombre.ilike(like))
            )

        # filtro por año
        anio = request.args.get("anio")
        if anio and anio.isdigit():
            query = query.filter(Pelicula.anio == int(anio))

        # filtro por género (puede ser id o nombre)
        genero = request.args.get("genero")
        if genero:
            if genero.isdigit():
                query = query.join(Pelicula.generos).filter(Genero.id_genero == int(genero))
            else:
                query = query.join(Pelicula.generos).filter(Genero.nombre.ilike(genero))

        destacadas = request.args.get("destacadas")

        if destacadas is not None:
            query = query.filter_by(destacada=True)
            schema = PeliculaDetalleSchema(many=True)
        else:
            schema = PeliculaListaSchema(many=True)
        
        peliculas = query.all()
        return jsonify(schema.dump(peliculas))
    
    def post(self):
        pelicula_schema = PeliculaSchema()
        detalle_schema = PeliculaDetalleSchema()

        form_data = request.form.to_dict()
        form_data["generos"] = request.form.getlist("generos")
        form_data["actores"] = request.form.getlist("actores")        

        poster = request.files.get("poster")
        banner = request.files.get("banner")

        errors = {}
        try:
            datos = pelicula_schema.load(form_data)
        except ValidationError  as err:
            errors.update(err.messages)

        # Validación de archivos
        for archivo, nombre in [(poster, "poster"), (banner, "banner")]:
            errors.update(validate_file(archivo, nombre))

        if errors:
            return {"errors": errors}, 400
        
        pelicula = Pelicula(
            nombre = datos["nombre"],
            anio = datos["anio"],
            puntuacion = datos["puntuacion"],
            duracion = datos["duracion"],
            sinopsis = datos["sinopsis"],
            slug = slugify(datos["nombre"]),
        )

        pelicula.generos = Genero.query.filter(Genero.id_genero.in_(form_data["generos"])).all()
        pelicula.actores = Actor.query.filter(Actor.id_actor.in_(form_data["actores"])).all()
        
        pelicula.poster = save_file(poster, "posters", pelicula.slug)
        pelicula.banner = save_file(banner, "banners", pelicula.slug)
        
        db.session.add(pelicula)
        db.session.commit()


        return jsonify(msg='Pelicula Creada', pelicula=detalle_schema.dump(pelicula))
    
class PeliculaResource(Resource):
    def get(self, pelicula_id):
        pelicula = Pelicula.query.get_or_404(pelicula_id)
        detalle_schema = PeliculaDetalleSchema()
        return jsonify(detalle_schema.dump(pelicula))


    def delete(self, pelicula_id):
        pelicula = Pelicula.query.get_or_404(pelicula_id)

        delete_file(pelicula.poster)
        delete_file(pelicula.banner)

        db.session.delete(pelicula)
        db.session.commit()
        return jsonify(msg='Pelicula Eliminada')
    
    def put(self, pelicula_id):
        pelicula_schema = PeliculaSchema(partial=True)
        detalle_schema = PeliculaDetalleSchema()
        pelicula = Pelicula.query.get_or_404(pelicula_id)

        form_data = request.form.to_dict()
        form_data["generos"] = request.form.getlist("generos")
        form_data["actores"] = request.form.getlist("actores")        

        poster = request.files.get("poster")
        banner = request.files.get("banner")

        errors = {}
        try:
            datos = pelicula_schema.load(form_data | {"id_pelicula": pelicula_id})
        except ValidationError  as err:
            errors.update(err.messages)

        for archivo, nombre in [(poster, "poster"), (banner, "banner")]:
            if not archivo:
                errors.update(validate_file(archivo, nombre))

        if errors:
            return {"errors": errors}, 400
        
        # actualizar atributos
        for campo in ["nombre", "anio", "puntuacion", "duracion", "sinopsis"]:
            if campo in datos:
                setattr(pelicula, campo, datos[campo])

        if "nombre" in datos: 
            pelicula.slug= slugify(datos["nombre"])
        
        if "generos" in datos:
            pelicula.generos = Genero.query.filter(Genero.id_genero.in_(datos["generos"])).all()
        if "actores" in datos:
            pelicula.actores = Actor.query.filter(Actor.id_actor.in_(datos["actores"])).all()   

        # actualizar imágenes si llegan nuevas
        if poster:
            pelicula.poster = save_file(poster, "posters", pelicula.slug, old_file=pelicula.poster)
        if banner:
            pelicula.banner = save_file(banner, "banners", pelicula.slug, old_file=pelicula.banner)

        db.session.commit()
        return jsonify(msg='Pelicula Actualizada',pelicula=detalle_schema.dump(pelicula))
