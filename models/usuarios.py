from typing import Optional
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
import enum
from sqlalchemy import DateTime, Enum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions import db, pwd_context

class UsuarioRol(enum.StrEnum):
    USUARIO="usuario"
    ADMIN="admin"

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id_usuario: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(db.String(100), nullable=False)
    correo: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    _contrasena: Mapped[str] = mapped_column("contrasena", db.String(255), nullable=False)
    rol: Mapped[UsuarioRol] = mapped_column(
        Enum(UsuarioRol),
        nullable=False,
        default=UsuarioRol.USUARIO
    )
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False,
        default=datetime.utcnow
    )

    tokens: Mapped[list["ListaTokens"]] = relationship(
        "ListaTokens", back_populates="usuario", cascade="all, delete-orphan"
    )

    @hybrid_property
    def contrasena(self):
        return self._contrasena

    @contrasena.setter
    def contrasena(self, contrasena):
        self._contrasena = pwd_context.hash(contrasena)


class ListaTokens(db.Model):
    __tablename__ = "lista_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    identificador_unico: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    tipo_de_token: Mapped[str] = mapped_column(String(10), nullable=False)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=False, index=True)
    anulado_en: Mapped[Optional[datetime]] = mapped_column(DateTime)
    expira: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="tokens")