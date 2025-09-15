import os
from flask import Flask, send_from_directory
from api.views import api_blueprint
from auth.views import auth_blueprint
from config import Config
from extensions import db, cors, jwt
from seed import llenar_datos_iniciales
from models.usuarios import Usuario

app = Flask(
    __name__,
    static_folder=Config.FRONTEND_FOLDER,
    static_url_path="/"
)
app.config.from_object(Config)

app.register_blueprint(api_blueprint)
app.register_blueprint(auth_blueprint)

db.init_app(app)
cors.init_app(app, supports_credentials=True, origins="*")
jwt.init_app(app)

# Ruta para servir archivos y subcarpetas dentro de /static/img
@app.route("/img/<path:filename>")
def uploaded_files(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)


# Rutas Angular
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_angular(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")
    
@app.errorhandler(404)
def not_found(e):
    request_path = str(getattr(e, "description", ""))

    if request_path.startswith("/api") or request_path.startswith("/auth"):
        return {"error": "Recurso no encontrado"}, 404
    
    if request_path.startswith("/img"):
        return {"error": "Imagen no encontrada"}, 404

    return send_from_directory(app.static_folder, "index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        llenar_datos_iniciales()
    app.run(debug=True)
    