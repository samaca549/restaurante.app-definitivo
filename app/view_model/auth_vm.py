
from app.model.data.db_repo import DbRepo 
from app.model.data.auth_repo import AuthRepo

from app.model.domain.usuario import Usuario

class AuthViewModel:
    
    def __init__(self, auth_repo: AuthRepo, db_repo: DbRepo):
        self.auth_repo = auth_repo
        self.db_repo = db_repo
        self.usuario_actual = None # Almacena la sesión

    def intentar_login(self, email, password):
        """
        Intenta autenticar al usuario y, si tiene éxito, carga sus datos
        desde la base de datos (DbRepo).
        """

        uid, resultado = self.auth_repo.login_usuario(email, password)
        
        if not uid:
            return f"Error: {resultado}" 
            
        # 3. Buscamos los datos completos del usuario en Firestore
        rol_db, nombre_db = self.db_repo.obtener_datos_usuario(uid) 
        
        if not rol_db or not nombre_db:
            return f"Error: Usuario autenticado (UID: {uid}), pero no se encontraron sus datos (rol/nombre) en la base de datos."

        # 4. Guardamos el usuario en la sesión
        self.usuario_actual = Usuario(uid, email, nombre_db, rol_db)
        return f"Login exitoso. Bienvenido, {nombre_db}. Tu rol es: {rol_db.upper()}"
        

    def registrar_usuario_y_rol(self, email: str, password: str, nombre: str, rol: str):
        """ 
        Registra el usuario en Auth y guarda sus datos en Firestore.
        Esta función ahora solo es llamada por un Administrador desde la UI.
        """
        
        try:

            uid = self.auth_repo.crear_usuario(email, password, rol, nombre)
            
            if "Error:" in str(uid):
                return uid 
            exito_db = self.db_repo.crear_registro_usuario(uid, email, nombre, rol)
            
            if not exito_db:

                 print(f"ERROR CRÍTICO: Falló el registro en DB. Revirtiendo creación en Auth para UID {uid}")
                 self.auth_repo.eliminar_usuario_auth(uid) # (Necesitarás implementar esto en AuthRepo)
                 return "Error: Falló el guardado en Base de Datos. Se revirtió la creación de Auth."

            return f"Usuario {email} creado con éxito y rol '{rol}' asignado."
            
        except Exception as e:
            return f"Error inesperado en ViewModel al registrar: {e}"

    
    def cerrar_sesion(self):
        """ Cierra la sesión borrando el usuario actual. """
        self.usuario_actual = None
        return "Sesión cerrada."
        
    def verificar_rol_acceso(self, roles_permitidos: list) -> bool:
        """ 
         Lógica de permisos actualizada.
        Verifica si el usuario actual tiene permiso.
        """
        if not self.usuario_actual:
            return False
            
        rol_actual = self.usuario_actual.rol.lower()
        
        if rol_actual == 'administrador':
            return True

        if rol_actual == 'gerente' and 'administrador' not in roles_permitidos:
            return True

        return rol_actual in roles_permitidos
