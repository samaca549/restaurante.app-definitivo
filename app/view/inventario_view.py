# app/view/inventario_view.py

class InventarioView:
    def mostrar_menu_inventario(self):
        raise NotImplementedError

    def obtener_datos_nuevo_producto(self):
        raise NotImplementedError
        
    def obtener_id_producto(self, accion="eliminar"):
        raise NotImplementedError

    def mostrar_resultado(self, resultado):
        raise NotImplementedError