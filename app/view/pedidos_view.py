# app/view/pedidos_view.py
# Define QUÉ debe hacer la vista de pedidos (pero no CÓMO)

class PedidosView:
    def mostrar_menu_pedidos(self):
        """ Muestra el menú de la sección Pedidos """
        raise NotImplementedError

    def obtener_datos_nuevo_pedido(self):
        """ Pide al usuario los datos para crear un pedido """
        raise NotImplementedError

    def obtener_id_pedido(self, accion="consultar"):
        """ Pide al usuario un ID de pedido """
        raise NotImplementedError

    def mostrar_resultado(self, resultado):
        """ Muestra un mensaje (éxito o error) """
        raise NotImplementedError