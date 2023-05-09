from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from app.controllers.controller import archivos_bp
from app.config.settings import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configuración de CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
app.register_blueprint(archivos_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=9000)
