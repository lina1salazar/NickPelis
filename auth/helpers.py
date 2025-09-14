from datetime import datetime
from flask_jwt_extended import decode_token
from config import Config
from models.usuarios import ListaTokens
from extensions import db


def agregar_token_a_lista(token_codificado):
    token_decodificado= decode_token(token_codificado)
    identificador_unico= token_decodificado["jti"]
    tipo_de_token= token_decodificado["type"]
    id_usuario= token_decodificado[Config.JWT_IDENTITY_CLAIM]
    expira= datetime.fromtimestamp(token_decodificado["exp"])

    token = ListaTokens(
        identificador_unico= identificador_unico, 
        tipo_de_token= tipo_de_token,
        id_usuario= id_usuario,
        expira= expira
    )
    db.session.add(token)
    db.session.commit()

def eliminar_tokens_de_usuario(id_usuario):
    ListaTokens.query.filter_by(id_usuario=id_usuario).delete()
    db.session.commit()

def token_existe(identificador_unico):
    return ListaTokens.query.filter_by(identificador_unico=identificador_unico).first()