# app/view_model/personal_vm.py

class PersonalViewModel:
    
    def __init__(self, db_repo):
        """
        Inicializa el ViewModel de Personal.
        Asumimos que el DbRepo general maneja la colección 'usuarios' donde está el personal.
        """
        self.db_repo = db_repo
        
    # ✅ --- EL MÉTODO QUE FALTABA (Opción 1) --- ✅
    def listar_personal(self):
        """
        Obtiene y lista todos los empleados registrados en la colección 'usuarios'.
        """
        if not self.db_repo.is_ready:
            return "Error: Conexión a la base de datos no disponible."
            
        try:
            # Asumimos que DbRepo tiene un método para obtener todos los documentos de una colección
            personal_docs = self.db_repo.obtener_todos_los_documentos('usuarios') 
            
            if not personal_docs:
                return "No hay personal registrado en el sistema."
            
            respuesta = "==== LISTA DE EMPLEADOS ====\n"
            respuesta += f"{'ID Interno (UID)':<25}{'Nombre':<30}{'Puesto (Rol)':<15}{'Salario (Mensual)':<20}\n"
            respuesta += "-" * 90 + "\n"
            
            # Formateamos la salida
            for uid, datos in personal_docs.items():
                nombre = datos.get('nombre', 'N/A')
                rol = datos.get('rol', 'N/A').upper()
                salario = datos.get('salario', 0.0)
                
                # Formateo del salario (asumiendo que se almacena)
                salario_str = f"${salario:,.2f}" if isinstance(salario, (int, float)) and salario > 0 else "N/A"
                
                respuesta += f"{uid[:20]}...{uid[-4:]:<4}{nombre:<30}{rol:<15}{salario_str:<20}\n"

            # Nota: El salario no se almacena automáticamente en el AuthVM/DbRepo que creamos antes, 
            # por lo que podría aparecer como 0.0 o N/A si no se usa 'Contratar nuevo empleado'.
            respuesta += "\nNota: Si no se ve el salario, use 'Contratar nuevo empleado' (Opción 2) para establecerlo."
            return respuesta
            
        except Exception as e:
            return f"Error al listar el personal: {e}"

    def contratar_empleado(self, nombre, puesto, salario):
        """
        Opción 2: Registra datos adicionales de salario y puesto para un empleado existente.
        Nota: El registro inicial de usuario (email/pass) debe hacerse desde el menú principal (Opción 2).
        """
        if not self.db_repo.is_ready:
            return "Error: Conexión a la base de datos no disponible."

        if salario <= 0:
            return "Error: El salario debe ser un número positivo."
        
        # Primero, necesitamos encontrar el UID del usuario por su nombre.
        # Esto es complejo si varios usuarios tienen el mismo nombre.
        # Por simplicidad, asumiremos que el nombre es único o se buscará el primero.
        try:
            personal_docs = self.db_repo.obtener_todos_los_documentos('usuarios')
            target_uid = None
            
            for uid, datos in personal_docs.items():
                if datos.get('nombre', '').lower().strip() == nombre.lower().strip():
                    target_uid = uid
                    break
            
            if not target_uid:
                return f"Error: No se encontró un usuario registrado con el nombre '{nombre}'. Asegúrate de registrarlo primero."
                
            # Actualizamos el documento con los nuevos datos
            datos_contrato = {'puesto': puesto.lower(), 'salario': salario}
            
            # Asumimos que el rol ya fue definido en el registro de usuario, por lo que 
            # sólo actualizamos 'puesto' (si es diferente al rol) y 'salario'.
            exito = self.db_repo.actualizar_documento('usuarios', target_uid, datos_contrato)
            
            if exito:
                return f"Contrato exitoso: Datos de '{nombre}' actualizados. Puesto: {puesto}, Salario: ${salario:,.2f}"
            else:
                return "Error al actualizar los datos del empleado en la base de datos."
                
        except Exception as e:
            return f"Error al contratar/actualizar empleado: {e}"


    def despedir_empleado(self, nombre):
        """
        Opción 3: Elimina permanentemente a un empleado del sistema (colección 'usuarios').
        """
        if not self.db_repo.is_ready:
            return "Error: Conexión a la base de datos no disponible."
            
        try:
            # Buscar el UID por nombre (misma lógica que contratar)
            personal_docs = self.db_repo.obtener_todos_los_documentos('usuarios')
            target_uid = None
            
            for uid, datos in personal_docs.items():
                if datos.get('nombre', '').lower().strip() == nombre.lower().strip():
                    target_uid = uid
                    break
            
            if not target_uid:
                return f"Error: No se encontró un usuario registrado con el nombre '{nombre}'."

            # Impedir que se despida el usuario 'gerente' principal
            if datos.get('rol', '').lower() == 'gerente' and nombre.lower().strip() == 'miguel samaca': 
                 return "Error: No se puede despedir al Gerente Principal del sistema."
            
            # Eliminamos el documento
            exito = self.db_repo.eliminar_documento('usuarios', target_uid)
            
            if exito:
                return f"Despido exitoso: El empleado '{nombre}' ha sido eliminado del sistema."
            else:
                return "Error al eliminar al empleado de la base de datos."
                
        except Exception as e:
            return f"Error al despedir empleado: {e}"