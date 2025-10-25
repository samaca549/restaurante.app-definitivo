class Usuario:
    """Clase de dominio para representar un usuario activo en el sistema."""
    def __init__(self, uid: str, email: str, nombre: str, rol: str):
        self.uid = uid
        self.email = email
        self.nombre = nombre
        self.rol = rol
        