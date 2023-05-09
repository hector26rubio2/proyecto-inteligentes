from flask import Blueprint, jsonify, request
from app.services.servicio import MiServicio

archivos_bp = Blueprint('archivos_bp', __name__)
servicio = MiServicio()


@archivos_bp.route('/', methods=['GET'])
def obtener_archivos():

    return "asdasd"


@archivos_bp.route('/archivo/upload/', methods=['POST'])
def cargar_archivo():
    try:
        archivo = request.files['file']
        if archivo:
            data = servicio.cargar_archivo(archivo)
            return jsonify({data[2]: data[0]}), data[1]
        else:
            return jsonify({'error': 'No se recibió ningún archivo.'}), 400
    except:
        return jsonify({'error': 'internal server error'}), 500


@archivos_bp.route('/archivos/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    nuevo_usuario = request.json
    servicio.actualizar_usuario(id, nuevo_usuario)
    return '', 204


@archivos_bp.route('/archivos/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    servicio.eliminar_usuario(id)
    return '', 204
