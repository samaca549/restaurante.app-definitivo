# app/model/data/auth_repo.py

from firebase_admin import auth as firebase_auth
from firebase_admin import exceptions

class AuthRepo:
    
    def __init__(self, auth_client: firebase_auth, is_ready_status: bool):
        """
        Inicializa el repositorio de autenticación.
        """
        self.auth_client = auth_client
        self._is_ready = is_ready_status
        
        if not self._is_ready:
                print("❌ ATENCIÓN: AuthRepo inicializado, pero el servicio de autenticación no está listo.")

    @property
    def is_ready(self):
        """ Propiedad para verificar el estado de la conexión. """
        return self._is_ready

    def login_usuario(self, email: str, password: str) -> tuple[str | None, str | None]:
        """ 
        Simula login usando Admin SDK (Solo valida existencia de email).
        En un sistema real, el Admin SDK no debe usarse para login de clientes.
        Retorna (uid, rol) o (None, mensaje_error).
        """
        if not self.is_ready:
            return None, "Error de conexión."

        try:
            # 1. Obtener el usuario por email (DESDE EL SERVICIO AUTH)
            user = self.auth_client.get_user_by_email(email)
            
            # (El Admin SDK no valida la contraseña, asumimos que es correcta si el email existe)
            
            # 2. Obtenemos el rol desde los Custom Claims
            # (El rol en Auth es la fuente de verdad para la seguridad)
            rol = user.custom_claims.get('rol', 'cajero') if user.custom_claims else 'cajero'
            
            return user.uid, rol
            
        except firebase_auth.UserNotFoundError:
            return None, "Usuario no encontrado o credenciales inválidas."
        except Exception as e:
            return None, f"Error inesperado en login: {e}"

    def crear_usuario(self, email: str, password: str, rol: str = "cajero", nombre: str = "") -> str | str:
        """ 
        Crea el usuario en Firebase Authentication (Admin SDK) y le asigna un rol
        como un Custom Claim.
        """
        if not self.is_ready: return "Error de conexión."
            
        try:
            # 1. Crea el usuario en Firebase Auth
            user = self.auth_client.create_user(
                email=email, 
                password=password,
                display_name=nombre
            )
            
            # 2. Establece el Custom Claim para el rol (MUY IMPORTANTE)
            self.auth_client.set_custom_user_claims(user.uid, {'rol': rol})
            
            return user.uid
        
        except exceptions.InvalidArgumentError as e:
            return f"Error de Argumento: {e}. Contraseña debe ser >= 6. Email debe ser válido."
        except firebase_auth.EmailAlreadyExistsError:
            return "Error: El email ya está registrado."
        except Exception as e:
            return f"Error al crear usuario: {e}"

    # ✅ --- MÉTODO AÑADIDO PARA DESPEDIR EMPLEADOS --- ✅
    def eliminar_usuario_auth(self, uid: str) -> bool:
        """
        Elimina un usuario de Firebase Authentication (para Rollback o Despido).
        """
        if not self.is_ready: 
            print(f"Error AuthRepo: No listo para eliminar {uid}")
            return False
        try:
            self.auth_client.delete_user(uid)
            print(f"Info AuthRepo: Usuario {uid} eliminado de Authentication.")
            return True
        except firebase_auth.UserNotFoundError:
             # Si el usuario ya no existe en Auth, igual es un "éxito"
            print(f"Info AuthRepo: Usuario {uid} ya estaba eliminado de Authentication.")
            return True
        except Exception as e:
            print(f"ERROR AuthRepo: Fallo al eliminar usuario {uid} de Auth: {e}")
            return False