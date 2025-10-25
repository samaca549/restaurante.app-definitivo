# app/model/domain/pedido.py
# Define los "moldes" para los datos de pedidos e inventario

class Pedido:
    """ Representa un Pedido. Es solo un molde de datos """
    def __init__(self, id_pedido, cliente, productos, total, estado="pendiente"):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.productos = productos  # Esto será una lista de diccionarios
        self.total = total
        self.estado = estado

    def a_diccionario(self):
        """ Convierte el objeto a un diccionario para guardarlo en Firebase """
        return {
            "id_pedido": self.id_pedido,
            "cliente": self.cliente,
            "productos": self.productos,
            "total": self.total,
            "estado": self.estado
        }

class ProductoInventario:
    """ Representa un producto en nuestro inventario """
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def a_diccionario(self):
        """ Convierte el producto a diccionario para Firebase """
        return {
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock
        }