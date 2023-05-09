from app.config.database import db


class Usuario:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo

    def guardar(self):
        db.usuarios.insert_one({
            'nombre': self.nombre,
            'correo': self.correo
        })

    @staticmethod
    def obtener_todos():
        return list(db.usuarios.find())

    @staticmethod
    def obtener_por_id(id):
        return db.usuarios.find_one({'_id': ObjectId(id)})

    def actualizar(self):
        db.usuarios.update_one(
            {'_id': self._id},
            {'$set': {
                'nombre': self.nombre,
                'correo': self.correo
            }}
        )

    def eliminar(self):
        db.usuarios.delete_one({'_id': self._id})
