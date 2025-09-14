from marshmallow import ValidationError, validate, validates_schema, EXCLUDE
from marshmallow.fields import String
from extensions import ma
from models.usuarios import Usuario, UsuarioRol

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    nombre= String(
        required=True, 
        validate=[validate.Length(min=5, max=100)],
    )
    correo= String(
        required=True,
        validate=[validate.Email()]
    )
    rol= String(
        validate=[validate.OneOf([r.value for r in UsuarioRol])], 
        load_default= UsuarioRol.USUARIO
    )  

    @validates_schema
    def validate_unique_correo(self,data, **kwargs):
        correo_value= data.get("correo")
        if Usuario.query.filter_by(correo=correo_value).count():
            raise ValidationError(
                f"El correo {correo_value} ya esta registrado")
        
    class Meta: 
        model = Usuario
        load_instance = True
        exclude = ["_contrasena"]
        unknown= EXCLUDE

class UsuarioCrearSchema(UsuarioSchema):
    contrasena = String(
        required=True,
        validate=[
            validate.Regexp(
                r"^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,}$",
                error="La contraseña debe tener al menos 8 caracteres, y tener al menos 1 de cada uno de los siguientes: letra minúscula, letra mayúscula, carácter especial, número.",
            )
        ],
        error_messages={
            "required": "La contraseña es requerida",
            "invalid": "La contraseña debe tener al menos 8 caracteres, y tener al menos 1 de cada uno de los siguientes: letra minúscula, letra mayúscula, carácter especial, número.",
        }
    )

    class Meta(UsuarioSchema.Meta):
        exclude = UsuarioSchema.Meta.exclude + ["rol"]

        
    
    
