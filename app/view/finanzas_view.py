# app/view/finanzas_view.py

class FinanzasView:
    def mostrar_menu_finanzas(self):
        raise NotImplementedError

    def obtener_datos_movimiento(self, tipo):
        raise NotImplementedError

    def mostrar_resultado(self, resultado):
        raise NotImplementedError