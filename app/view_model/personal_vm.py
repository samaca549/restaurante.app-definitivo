# app/view_model/personal_vm.py

class PersonalViewModel:
    
    # ✅ CORRECCIÓN 1: El constructor ahora recibe ambos repositorios
    def __init__(self, auth_repo, db_repo):
        """
        Inicializa el ViewModel de Personal.
        Necesita AuthRepo para borrar usuarios de Authentication.
        Necesita DbRepo para borrar usuarios de Firestore ('usuarios').
        """
        self.auth_repo = auth_repo
        self.db_repo = db_repo
        
    def listar_personal(self):
        """
        Obtiene y lista todos los empleados registrados en la colección 'usuarios'.
        """
        if not self.db_repo.is_ready:
            return "Error: Conexión a la base de datos no disponible."
            
        try:
            personal_docs = self.db_repo.obtener_todos_los_documentos('usuarios') 
            
            if not personal_docs:
                return "No hay personal registrado en el sistema."
            
            respuesta = "==== LISTA DE EMPLEADOS ====\n"
            respuesta += f"{'ID Interno (UID)':<30}{'Nombre':<30}{'Puesto (Rol)':<15}\n"
            respuesta += "-" * 75 + "\n"
            
            for uid, datos in personal_docs.items():
                nombre = datos.get('nombre', 'N/A')
                rol = datos.get('rol', 'N/A').upper()
                respuesta += f"{uid:<30}{nombre:<30}{rol:<15}\n"

            return respuesta
            
        except Exception as e:
            return f"Error al listar el personal: {e}"

    def contratar_empleado(self, nombre, puesto, salario):
        """
        Actualiza el salario y puesto de un empleado existente en Firestore.
        """
        if not self.db_repo.is_ready:
            return "Error: Conexión a la base de datos no disponible."

        if salario <= 0:
            return "Error: El salario debe ser un número positivo."
        
        try:
            # 1. Encontrar el UID del empleado por su nombre
            personal_docs = self.db_repo.obtener_todos_los_documentos('usuarios')
            if not personal_docs:
                 return "Error: No se pudo leer la lista de personal."

            target_uid = None
            for uid, datos in personal_docs.items():
                if datos.get('nombre', '').lower().strip() == nombre.lower().strip():
                    target_uid = uid
                    break
            
            if not target_uid:
                return f"Error: No se encontró un usuario registrado con el nombre '{nombre}'."
                
            # 2. Actualizamos el documento en Firestore
            datos_contrato = {'puesto': puesto.lower(), 'salario': salario}
            exito = self.db_repo.actualizar_documento('usuarios', target_uid, datos_contrato)
            
            if exito:
                return f"Contrato exitoso: Datos de '{nombre}' actualizados. Puesto: {puesto}, Salario: ${salario:,.2f}"
            else:
                return "Error al actualizar los datos del empleado en la base de datos."
                
        except Exception as e:
            return f"Error al contratar/actualizar empleado: {e}"

    # ✅ CORRECCIÓN 2: Lógica de despido actualizada
    def despedir_empleado(self, nombre):
        """
        Elimina permanentemente a un empleado de Firestore Y de Authentication.
        """
        if not self.db_repo.is_ready or not self.auth_repo.is_ready:
            return "Error: Los repositorios de datos no están listos."

        try:
            # 1. Encontrar el UID del empleado por su nombre
            personal_docs = self.db_repo.obtener_todos_los_documentos('usuarios')
            if not personal_docs:
                    return "Error: No se pudo leer la lista de personal."

            target_uid = None
            target_email = None
            
            for uid, datos in personal_docs.items():
                if datos.get('nombre', '').lower().strip() == nombre.lower().strip():
                    target_uid = uid
                    target_email = datos.get('email', 'N/A')
                    break
            
            if not target_uid:
                return f"Error: No se encontró un empleado con el nombre '{nombre}'."

            # 2. Iniciar el proceso de eliminación en dos pasos
            print(f"Iniciando despido de: {nombre} (UID: {target_uid})...")

            # 3. Eliminar de Firestore (Base de datos de perfiles)
            exito_db = self.db_repo.eliminar_documento('usuarios', target_uid)
            
            if not exito_db:
                # Si no se puede borrar de la DB, NO borramos de Auth.
                return f"Error CRÍTICO: Se encontró al empleado, pero no se pudo eliminar de Firestore (DB)."

            # 4. Eliminar de Firebase Authentication (Login)
            exito_auth = self.auth_repo.eliminar_usuario_auth(target_uid)

            if not exito_auth:
                # El perfil de DB se borró, pero el login no. Es una advertencia.
                return f"ADVERTENCIA: Empleado '{nombre}' eliminado de Firestore (DB), pero falló la eliminación de Authentication (Login).\nDebe eliminarse manualmente desde la consola de Firebase (Email: {target_email})."

            return f"✅ Despido completado. El empleado '{nombre}' ha sido eliminado de Firestore y de Authentication."

        except Exception as e:
            return f"Error inesperado durante el proceso de despido: {e}"