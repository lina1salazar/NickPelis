from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.context import CryptContext
from flask_cors import CORS

db=SQLAlchemy()
ma=Marshmallow()
pwd_context=CryptContext(schemes=["pbkdf2_sha256"], deprecated='auto')
jwt=JWTManager()
cors = CORS()