import datetime
import os
from flask import Blueprint, jsonify, request

my_routes = Blueprint('my_routes', __name__)


@my_routes.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        if file:
            filename = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S") + '_' + file.filename
            file.save(os.path.join('Archivos/', filename))
            return jsonify({'message': 'Archivo guardado exitosamente.'}), 200
        else:
            return jsonify({'error': 'No se recibió ningún archivo.'}), 400
    except:
        return jsonify({'error': 'internal erro.'}), 500
    
