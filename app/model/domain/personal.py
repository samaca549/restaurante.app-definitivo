
class Empleado:
    """ Representa a un empleado """
    def __init__(self, id_empleado, nombre, puesto, salario):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.puesto = puesto
        self.salario = salario

    def a_diccionario(self):
        return {
            "id_empleado": self.id_empleado,
            "nombre": self.nombre,
            "puesto": self.puesto,
            "salario": self.salario
        }
