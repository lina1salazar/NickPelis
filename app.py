from flask import Flask
from api.views import api_blueprint
from auth.views import auth_blueprint
from config import Config
from extensions import db, cors
from seed import llenar_datos_iniciales
from models.usuarios import Usuario

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(api_blueprint)
app.register_blueprint(auth_blueprint)

db.init_app(app)
cors.init_app(app, supports_credentials=True, origins="*")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        llenar_datos_iniciales()
    app.run(debug=True)
    