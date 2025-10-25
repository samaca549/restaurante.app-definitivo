# app/view/personal_view.py

class PersonalView:
    def mostrar_menu_personal(self):
        raise NotImplementedError

    def obtener_datos_empleado(self):
        raise NotImplementedError
        
    def obtener_id_empleado(self, accion="eliminar"):
        raise NotImplementedError

    def mostrar_resultado(self, resultado):
        raise NotImplementedError