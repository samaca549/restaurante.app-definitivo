# app/view/login_view.py

class LoginView:
    def mostrar_menu_inicio(self):
        """ Muestra el menú antes de iniciar sesión. """
        raise NotImplementedError

    def obtener_credenciales(self, modo="login"):
        """ Pide al usuario el email y password. """
        raise NotImplementedError

    def mostrar_resultado(self, resultado):
        """ Muestra un mensaje (éxito o error). """
        raise NotImplementedError