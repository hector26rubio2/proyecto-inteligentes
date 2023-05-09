from app.models.modelo import Usuario
from datetime import datetime
import os


class MiServicio:

    def cargar_archivo(self, archivo):
        try:
            filename = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S") + '_' + archivo.filename
            archivo.save(os.path.join('./app/documents/', filename))
            return ("Archivo guardado exitosamente", 200,"message")
        except :
            return ("No se pudo guardar el archivo", 500,"error")

    def obtener_usuarios(self):
        return Usuario.obtener_todos()

    def obtener_usuario_por_id(self, id):
        return Usuario.obtener_por_id(id)

    def actualizar_usuario(self, id, datos_usuario):
        usuario = Usuario.obtener_por_id(id)
        usuario.nombre = datos_usuario['nombre']
        usuario.correo = datos_usuario['correo']
        usuario.actualizar()

    def eliminar_usuario(self, id):
        usuario = Usuario.obtener_por_id(id)
        usuario.eliminar()
