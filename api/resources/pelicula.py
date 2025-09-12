from flask import jsonify, request
from flask_restful import Resource
from flask_restful import Resource
from marshmallow import ValidationError
from extensions import db

from api.schemas.pelicula import PeliculaSchema, PeliculaDetalleSchema, slugify
from models.peliculas import Pelicula, Genero, Actor

  
class PeliculasResource(Resource):
    def get(self):
        peliculas = Pelicula.query.all()
        peliculas_schema = PeliculaSchema(many = True)
        return jsonify(peliculas_schema.dump(peliculas))
    
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
            errors = err.messages

        print([poster, banner, errors])
        if not poster or not banner:
            errors["poster"] = ["Poster es requerido"]
            errors["banner"] = ["Banner es requerido"]

        for archivo, nombre in [(poster, "poster"), (banner, "banner")]:
            if not archivo:
                continue
            if archivo.mimetype not in ["image/jpeg", "image/png"]:
                errors[nombre] = ["Formato no soportado, solo se permite jpeg/png"]
            if(len(archivo.read()) > 2 * 1024 * 1024): # 2MB
                errors[nombre] = ["El archivo es muy grande (max 2MB)"]
            archivo.seek(0)

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

        if "generos" in request.json:
            pelicula.generos = Genero.query.filter(
                Genero.id_genero.in_(request.json["generos"])
            ).all()
        if "actores" in request.json:
            pelicula.actores = Actor.query.filter(
                Actor.id_actor.in_(request.json["actores"])
            ).all()

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
        db.session.delete(pelicula)
        db.session.commit()
        return jsonify(msg='Pelicula Eliminada')
    
    def put(self, pelicula_id):
        pelicula_schema = PeliculaSchema(partial=True)
        detalle_schema = PeliculaDetalleSchema()
        pelicula = Pelicula.query.get_or_404(pelicula_id)

        try:
            datos = pelicula_schema.load(request.json | {"id_pelicula": pelicula_id})
        except ValidationError  as err:
            return {"errors": err.messages}, 400
        
        for campo in ["nombre", "anio", "puntuacion", "duracion", "sinopsis"]:
            if campo in datos:
                setattr(pelicula, campo, datos[campo])

        if "nombre" in datos: 
            pelicula.slug= slugify(datos["nombre"])
        
        if "generos" in datos:
            pelicula.generos = Genero.query.filter(
                Genero.id_genero.in_(datos["generos"])
            ).all()
        if "actores" in datos:
            pelicula.actores = Actor.query.filter(
                Actor.id_actor.in_(datos["actores"])
            ).all()   

        db.session.commit()
        return jsonify(msg='Pelicula Actualizada',pelicula=detalle_schema.dump(pelicula))
