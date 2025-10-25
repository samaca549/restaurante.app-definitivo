# app/model/domain/finanzas.py

class MovimientoFinanciero:
    """ Representa un ingreso o un egreso """
    def __init__(self, id_mov, tipo, descripcion, monto, fecha):
        self.id_mov = id_mov
        self.tipo = tipo  # "ingreso" o "egreso"
        self.descripcion = descripcion
        self.monto = monto
        self.fecha = fecha

    def a_diccionario(self):
        return {
            "id_mov": self.id_mov,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "monto": self.monto,
            "fecha": self.fecha
        }