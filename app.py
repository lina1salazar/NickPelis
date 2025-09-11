from flask import Flask
from api.views import api_blueprint
from config import Config
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(api_blueprint)

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



