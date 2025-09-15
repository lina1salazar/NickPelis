from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    if DB_PASSWORD:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(BASE_DIR, "static")
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "img")
    FRONTEND_FOLDER = os.path.join(BASE_DIR, "dist", "pagina-peliculas", "browser")

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'supersecreto')
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_IDENTITY_CLAIM = "id_usuario" # default: sub
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
