from datetime import datetime
from typing import List
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions import db
from utils.timezone import now_bogota


class Genero(db.Model):
    __tablename__ = 'generos'
    id_genero: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(db.String(50), unique=True)

    peliculas: Mapped[List["Pelicula"]] = relationship(
        secondary="peliculas_generos",
        back_populates="generos",
        passive_deletes=True
    )


class Actor(db.Model):
    __tablename__ = 'actores'
    id_actor: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(db.String(100), unique=True)

    peliculas: Mapped[List["Pelicula"]] = relationship(
        secondary="peliculas_actores",
        back_populates="actores",
        passive_deletes=True
    )

class Pelicula(db.Model):
    __tablename__ = "peliculas"
    id_pelicula: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(db.String(150), nullable=False)
    anio: Mapped[int] = mapped_column(nullable=False)
    puntuacion: Mapped[float] = mapped_column(nullable=False)
    duracion: Mapped[int] = mapped_column(nullable=False)
    sinopsis: Mapped[str] = mapped_column(db.Text, nullable=False)
    poster: Mapped[str] = mapped_column(db.String(255), nullable=False)
    banner: Mapped[str] = mapped_column(db.String(255), nullable=False)
    destacada: Mapped[bool] = mapped_column(db.Boolean, default=False)
    
    generos: Mapped[List["Genero"]] = relationship(
        "Genero",
        secondary="peliculas_generos",
        back_populates="peliculas",
        passive_deletes=True
    )
    actores: Mapped[List["Actor"]] = relationship(
        "Actor",
        secondary="peliculas_actores",
        back_populates="peliculas",
        passive_deletes=True
    )

    comentarios: Mapped[list["Comentario"]] = relationship(
        "Comentario",
        back_populates="pelicula",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    

class PeliculaGenero(db.Model):
    __tablename__ = "peliculas_generos"
    id_pelicula: Mapped[int] = mapped_column(
        db.ForeignKey("peliculas.id_pelicula", ondelete="CASCADE"), primary_key=True
    )
    id_genero: Mapped[int] = mapped_column(
        db.ForeignKey("generos.id_genero", ondelete="CASCADE"), primary_key=True
    )

class PeliculaActor(db.Model):
    __tablename__ = "peliculas_actores"
    id_pelicula: Mapped[int] = mapped_column(
        db.ForeignKey("peliculas.id_pelicula", ondelete="CASCADE"), primary_key=True
    )
    id_actor: Mapped[int] = mapped_column(
        db.ForeignKey("actores.id_actor", ondelete="CASCADE"), primary_key=True
    )

class Comentario(db.Model):
    __tablename__ = "comentarios"
    id_comentario: Mapped[int] = mapped_column(primary_key = True)
    id_usuario: Mapped[int] = mapped_column(
        db.ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        nullable= False
    )
    id_pelicula: Mapped[int] = mapped_column(
        db.ForeignKey("peliculas.id_pelicula", ondelete="CASCADE"),
        nullable= False
    )
    contenido: Mapped[str] = mapped_column(db.Text, nullable= False)
    calificacion: Mapped[float] = mapped_column(nullable=False)
    fecha_comentario: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False,
        default=now_bogota
    )


    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="comentarios")
    pelicula: Mapped["Pelicula"] = relationship("Pelicula", back_populates="comentarios")
