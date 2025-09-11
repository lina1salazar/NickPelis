from sqlalchemy.orm import Mapped, mapped_column
from extensions import db


class Actor(db.Model):
    __tablename__ = 'actores'
    id_actor: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)
