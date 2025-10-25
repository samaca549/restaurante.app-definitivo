# app/model/data/auth_repo.py

from firebase_admin import auth as firebase_auth
from firebase_admin import exceptions

class AuthRepo:
    
    def __init__(self, auth_client: firebase_auth, is_ready_status: bool):
        self.auth_client = auth_client
        self._is_ready = is_ready_status
        
        if not self._is_ready:
                print("❌ ATENCIÓN: AuthRepo inicializado, pero el servicio de autenticación no está listo.")

    @property
    def is_ready(self):
        return self._is_ready

    def login_usuario(self, email: str, password: str) -> tuple[str | None, str | None]:
        """ 
        Simula login usando Admin SDK (Solo valida existencia de email).
        """
        if not self.is_ready:
            return None, "Error de conexión."

        try:
            # 1. Obtener el usuario por email (DESDE EL SERVICIO AUTH)
            user = self.auth_client.get_user_by_email(email)
            
            # (El Admin SDK no valida la contraseña, asumimos que es correcta si el email existe)
            
            # 2. Obtenemos el rol desde los Custom Claims
            rol = user.custom_claims.get('rol', 'cajero') if user.custom_claims else 'cajero'
            
            return user.uid, rol
            
        except firebase_auth.UserNotFoundError:
            return None, "Usuario no encontrado o credenciales inválidas."
        except Exception as e:
            return None, f"Error inesperado en login: {e}"

    def crear_usuario(self, email: str, password: str, rol: str = "cajero", nombre: str = "") -> str | str:
        """ 
        Crea el usuario en Firebase Authentication (Admin SDK) y le asigna un rol.
        """
        if not self.is_ready: return "Error de conexión."
            
        try:
            # 1. Crea el usuario en Firebase Auth
            user = self.auth_client.create_user(
                email=email, 
                password=password,
                display_name=nombre
            )
            
            # 2. Establece el Custom Claim para el rol
            # (Esto es crucial para la seguridad de Firebase)
            self.auth_client.set_custom_user_claims(user.uid, {'rol': rol})
            
            return user.uid
        
        except exceptions.InvalidArgumentError as e:
            return f"Error de Argumento: {e}. Contraseña debe ser >= 6. Email debe ser válido."
        except firebase_auth.EmailAlreadyExistsError:
            return "Error: El email ya está registrado."
        except Exception as e:
            return f"Error al crear usuario: {e}"

    def eliminar_usuario_auth(self, uid: str) -> bool:
        """
        ✅ NUEVO: Elimina un usuario de Firebase Auth (para Rollback).
        """
        if not self.is_ready: return False
        try:
            self.auth_client.delete_user(uid)
            return True
        except Exception as e:
            print(f"ERROR AUTH REPO: Fallo al eliminar usuario {uid} de Auth: {e}")
            return False