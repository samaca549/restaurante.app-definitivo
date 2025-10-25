import os 
# Se asume que las Vistas Abstractas (PedidosView, LoginView, etc.) existen en app/view/

class InterfazConsola: 
    
    def __init__(self, auth_vm, pedidos_vm, inventario_vm, finanzas_vm, personal_vm):
        self.auth_vm = auth_vm
        self.pedidos_vm = pedidos_vm
        self.inventario_vm = inventario_vm
        self.finanzas_vm = finanzas_vm
        self.personal_vm = personal_vm
        
    # --- UTILIDADES ---

    def _limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear') 

    def _pausa(self):
        input("\nPresiona Enter para continuar...")

    def mostrar_resultado(self, resultado):
        """ Muestra un resultado formateado (string, lista o dict) """
        print("\n--- Resultado ---")
        if isinstance(resultado, (str, bytes)):
            print(resultado)
        elif isinstance(resultado, list):
            if not resultado:
                print("No se encontraron resultados.")
            for item in resultado:
                print(f"- {item}") # Imprime listas como bullets
        elif isinstance(resultado, dict):
            if not resultado:
                print("No se encontraron resultados.")
            for key, value in resultado.items():
                print(f"{key}: {value}")
        else:
            # Para objetos o números
            print(resultado)
        print("-----------------")
        

    # --- IMPLEMENTACIÓN LOGIN/INICIO (Menú Corregido) ---
    
    def mostrar_menu_inicio(self):
        """ Muestra el menú antes de iniciar sesión. """
        while True:
            self._limpiar_pantalla()
            print("==== BIENVENIDO AL SISTEMA RESTAURANTE ====")
            print("1. Iniciar Sesión")
            # ✅ CORRECCIÓN: Opción 2 ahora es solo explicativa
            print("2. Registrar Nuevo Usuario (Ver información)")
            print("3. Salir")
            opcion = input("Selecciona una opción (1-3): ")

            if opcion == '1':
                email, password = self._obtener_datos_login() 
                if email and password:
                    # El AuthViewModel se encarga de loguear y guardar el usuario
                    resultado = self.auth_vm.intentar_login(email, password)
                    self.mostrar_resultado(resultado)
                
                    if "Login exitoso" in resultado:
                        # Si el login es bueno, vamos al menú principal
                        self.run_menu_principal() 
                self._pausa()

            elif opcion == '2':
                # ✅ CORRECCIÓN: Mensaje explicativo
                self.mostrar_resultado("La creación de usuarios está restringida.\nSolo un 'Administrador' puede crear nuevas cuentas desde su sesión.")
                self._pausa()
                
            elif opcion == '3':
                print("Gracias por usar el sistema. ¡Adiós!")
                return 
            else:
                self.mostrar_resultado("Opción no válida. Inténtalo de nuevo.")
                self._pausa()
                
    def _obtener_datos_login(self):
        print("\n--- INICIO DE SESIÓN ---")
        email = input("Email: ")
        password = input("Contraseña: ")
        return email, password
    
    def _obtener_datos_registro(self):
        """Función interna, ahora solo llamada por el Admin."""
        print("\n--- REGISTRO DE NUEVO USUARIO (ADMIN) ---")
        email = input("Email: ")
        password = input("Contraseña (mín. 6 caracteres): ")
        nombre = input("Nombre completo: ") 
        
        # ✅ CORRECCIÓN: Se añade el rol 'administrador'
        rol = input("Rol a asignar (administrador/gerente/cajero/cocinero): ").lower().strip()
        
        roles_validos = ['administrador', 'gerente', 'cajero', 'cocinero']
        if rol not in roles_validos:
            self.mostrar_resultado(f"Error: Rol no válido. Debe ser uno de: {', '.join(roles_validos)}.")
            return None, None, None, None
            
        if len(password) < 6:
            self.mostrar_resultado("Error: La contraseña debe tener al menos 6 caracteres.")
            return None, None, None, None
            
        return email, password, nombre, rol

    # --- MENÚ PRINCIPAL (CONTROL DE ROLES) ---
    
    def run_menu_principal(self):
        """
        ✅ NUEVO: Decide qué menú mostrar basado en el rol del usuario logueado.
        """
        if not self.auth_vm.usuario_actual:
            return # Seguridad: si no hay usuario, no muestra menú

        rol = self.auth_vm.usuario_actual.rol.lower()
        
        # Redirige al menú correspondiente
        if rol == 'administrador':
            self.run_menu_administrador()
        elif rol == 'gerente':
            self.run_menu_gerente()
        else: # Cajero o Cocinero
            self.run_menu_operativo()
            
    # --- MENÚS SEGÚN ROL ---
    
    def run_menu_administrador(self):
        """
        ✅ NUEVO: Menú exclusivo para el rol de Administrador.
        Tiene todo lo del Gerente MÁS la creación de usuarios.
        """
        nombre = self.auth_vm.usuario_actual.nombre
        while self.auth_vm.usuario_actual: # Bucle mientras la sesión esté activa
            self._limpiar_pantalla()
            print(f"Sesión activa: {nombre} (ADMINISTRADOR)")
            print("==== SISTEMA DE GESTIÓN (ADMIN) ====")
            print("1. Módulo de Pedidos")
            print("2. Módulo de Inventario")
            print("3. Módulo de Finanzas")
            print("4. Módulo de Personal")
            print("5. 🛡️ AGREGAR NUEVO USUARIO (ADMIN) 🛡️")
            print("9. Cerrar Sesión")
            
            opcion = input("Selecciona una opción: ")

            if opcion == '1':
                self.run_menu_pedidos()
            elif opcion == '2':
                self.run_menu_inventario()
            elif opcion == '3':
                self.run_menu_finanzas()
            elif opcion == '4':
                self.run_menu_personal()
            elif opcion == '5':
                # Llama a la función de registro que antes era pública
                datos_registro = self._obtener_datos_registro()
                if datos_registro[0]: # Si los datos son válidos
                    email, password, nombre_reg, rol_reg = datos_registro
                    resultado = self.auth_vm.registrar_usuario_y_rol(email, password, nombre_reg, rol_reg) 
                    self.mostrar_resultado(resultado)
                self._pausa()
            elif opcion == '9':
                self.auth_vm.cerrar_sesion()
                self.mostrar_resultado("Sesión cerrada correctamente.")
                return # Sale del bucle y vuelve al menú de inicio
            else:
                self.mostrar_resultado("Opción no válida.")
                self._pausa()

    def run_menu_gerente(self):
        """
        ✅ NUEVO: Menú exclusivo para el Gerente.
        (Igual que Admin, pero SIN la opción 5)
        """
        nombre = self.auth_vm.usuario_actual.nombre
        while self.auth_vm.usuario_actual:
            self._limpiar_pantalla()
            print(f"Sesión activa: {nombre} (GERENTE)")
            print("==== SISTEMA DE GESTIÓN (GERENTE) ====")
            print("1. Módulo de Pedidos")
            print("2. Módulo de Inventario")
            print("3. Módulo de Finanzas")
            print("4. Módulo de Personal")
            print("9. Cerrar Sesión")
            
            opcion = input("Selecciona una opción: ")

            if opcion == '1':
                self.run_menu_pedidos()
            elif opcion == '2':
                self.run_menu_inventario()
            elif opcion == '3':
                self.run_menu_finanzas()
            elif opcion == '4':
                self.run_menu_personal()
            elif opcion == '9':
                self.auth_vm.cerrar_sesion()
                return 
            else:
                self.mostrar_resultado("Opción no válida.")
                self._pausa()

    def run_menu_operativo(self):
        """
        ✅ NUEVO: Menú para Cajero y Cocinero.
        Muestra opciones según el rol específico.
        """
        nombre = self.auth_vm.usuario_actual.nombre
        rol = self.auth_vm.usuario_actual.rol.lower()
        while self.auth_vm.usuario_actual:
            self._limpiar_pantalla()
            print(f"Sesión activa: {nombre} ({rol.upper()})")
            print("==== SISTEMA DE GESTIÓN (OPERATIVO) ====")
            
            opciones = {}
            i = 1

            # Módulo de Pedidos (Todos los roles operativos)
            opciones[str(i)] = ("Módulo de Pedidos", self.run_menu_pedidos)
            print(f"{i}. Módulo de Pedidos")
            i += 1

            # Módulo de Inventario (Solo Cocinero)
            if rol == 'cocinero':
                opciones[str(i)] = ("Módulo de Inventario", self.run_menu_inventario)
                print(f"{i}. Módulo de Inventario")
                i += 1

            print("9. Cerrar Sesión")
            opcion = input("Selecciona una opción: ")

            if opcion == '9':
                self.auth_vm.cerrar_sesion()
                return 

            if opcion in opciones:
                opciones[opcion][1]() # Llama a la función del menú
            else:
                self.mostrar_resultado("Opción no válida o no tienes permisos.")
                self._pausa()

    # ----------------------------------------------------------------
    # --- MÓDULO DE PEDIDOS (Mejora para Cajero) ---
    # ----------------------------------------------------------------

    def run_menu_pedidos(self):
        """Menú para la gestión de pedidos."""
        rol = self.auth_vm.usuario_actual.rol.lower()
        
        while True:
            self._limpiar_pantalla()
            print("==== MÓDULO DE PEDIDOS ====")
            
            opciones = {}
            i = 1

            # Opciones de Cajero
            if rol in ['administrador', 'gerente', 'cajero']:
                opciones[str(i)] = ("Tomar Nuevo Pedido", self._tomar_nuevo_pedido)
                print(f"{i}. Tomar Nuevo Pedido (Cajero)")
                i += 1
                opciones[str(i)] = ("Finalizar Pedido (Cobrar)", self._finalizar_pedido)
                print(f"{i}. Finalizar Pedido (Cobrar)")
                i += 1
            
            # Opciones de Cocina
            if rol in ['administrador', 'gerente', 'cocinero']:
                opciones[str(i)] = ("Ver Pedidos Activos (Cocina)", lambda: self.mostrar_resultado(self.pedidos_vm.ver_pedidos_activos()))
                print(f"{i}. Ver Pedidos Activos (Cocina)")
                i += 1
                
            print("9. Volver al Menú Principal")
            
            opcion = input("Selecciona una opción: ")

            if opcion == '9':
                return
            if opcion in opciones:
                opciones[opcion][1]() # Llama a la función
            else:
                self.mostrar_resultado("Opción no válida o no tienes permisos.")
            self._pausa()

    def _tomar_nuevo_pedido(self):
        # ... (Esta función está correcta como estaba)
        self._limpiar_pantalla()
        print("--- TOMAR NUEVO PEDIDO ---")
        menu = self.pedidos_vm.obtener_menu()
        self.mostrar_resultado(menu)
        items = []
        while True:
            item_id = input("Introduce el ID del plato (o 'fin' para terminar): ")
            if item_id.lower() == 'fin':
                break
            try:
                cantidad = int(input(f"Cantidad de plato ID '{item_id}': "))
                if cantidad > 0:
                    items.append({'item_id': item_id, 'cantidad': cantidad})
                else:
                    self.mostrar_resultado("La cantidad debe ser mayor a cero.")
            except ValueError:
                self.mostrar_resultado("Entrada inválida. Debe ser un número entero.")
        if items:
            resultado = self.pedidos_vm.crear_pedido(items, self.auth_vm.usuario_actual.uid)
            self.mostrar_resultado(resultado)
        else:
            self.mostrar_resultado("Pedido cancelado: No se agregaron productos.")

    def _finalizar_pedido(self):
        """
        ✅ MEJORA: Muestra los pedidos activos para facilitar la selección del ID.
        """
        self._limpiar_pantalla()
        print("--- FINALIZAR PEDIDO (COBRAR) ---")
        print("Mostrando pedidos que están listos para cobro ('ACTIVO'):\n")
        
        # 1. Muestra la lista de pedidos
        pedidos_activos_str = self.pedidos_vm.ver_pedidos_activos()
        self.mostrar_resultado(pedidos_activos_str)
        
        if "No hay pedidos activos" in pedidos_activos_str:
            return # No hay nada que finalizar

        # 2. Pide el ID
        pedido_id = input("\nIntroduce el ID del pedido a finalizar/cobrar: ")
        if not pedido_id:
            self.mostrar_resultado("Cancelado.")
            return

        resultado = self.pedidos_vm.finalizar_pedido(pedido_id)
        self.mostrar_resultado(resultado)

    # ----------------------------------------------------------------
    # --- MÓDULOS DE INVENTARIO, FINANZAS Y PERSONAL ---
    # (Estas funciones están correctas y no necesitan cambios)
    # ----------------------------------------------------------------

    def run_menu_inventario(self):
        # (Sin cambios, asumiendo que ya funciona)
        rol = self.auth_vm.usuario_actual.rol.lower()
        while True:
            self._limpiar_pantalla()
            print("==== MÓDULO DE INVENTARIO ====")
            print("1. Listar todo el inventario")
            print("2. Buscar producto por nombre")
            if rol in ["administrador", "gerente"]:
                print("3. Agregar/Actualizar producto")
                print("4. Eliminar producto")
            print("9. Volver al menú principal")
            opcion = input("Selecciona una opción: ")
            if opcion == '1':
                self.mostrar_resultado(self.inventario_vm.listar_inventario())
            elif opcion == '2':
                nombre = input("Nombre del producto a buscar: ")
                self.mostrar_resultado(self.inventario_vm.buscar_producto(nombre))
            elif opcion == '3' and rol in ["administrador", "gerente"]:
                nombre, cantidad, precio = self._obtener_datos_producto()
                if nombre and cantidad is not None and precio is not None:
                    self.mostrar_resultado(self.inventario_vm.agregar_o_actualizar_producto(nombre, cantidad, precio))
            elif opcion == '4' and rol in ["administrador", "gerente"]:
                nombre = input("Nombre del producto a eliminar: ")
                self.mostrar_resultado(self.inventario_vm.eliminar_producto(nombre))
            elif opcion == '9':
                break
            else:
                self.mostrar_resultado("Opción no válida o sin permisos.")
            self._pausa()

    def _obtener_datos_producto(self):
        # (Sin cambios)
        print("\n--- Datos del Producto ---")
        nombre = input("Nombre del producto: ")
        try:
            cantidad = float(input("Cantidad en stock (unidades, kg, L): "))
            precio = float(input("Precio unitario de COSTO: "))
            return nombre, cantidad, precio
        except ValueError:
            self.mostrar_resultado("Error: Cantidad y Precio deben ser números.")
            return None, None, None

    def run_menu_finanzas(self):
        # (Sin cambios, asumiendo que ya funciona)
        while True:
            self._limpiar_pantalla()
            print("==== MÓDULO DE FINANZAS (GERENTE/ADMIN) ====")
            print("1. Calcular ingresos totales del día")
            print("2. Ver reporte de gastos y movimientos")
            print("3. Registrar nuevo gasto (Egreso)")
            print("9. Volver al menú principal")
            opcion = input("Selecciona una opción: ")
            if opcion == '1':
                self.mostrar_resultado(self.finanzas_vm.calcular_ingresos_del_dia())
            elif opcion == '2':
                self.mostrar_resultado(self.finanzas_vm.obtener_reporte_gastos())
            elif opcion == '3':
                descripcion, monto_str = self._obtener_datos_gasto()
                if descripcion and monto_str is not None:
                    self.mostrar_resultado(self.finanzas_vm.registrar_gasto(descripcion, monto_str))
            elif opcion == '9':
                break
            else:
                self.mostrar_resultado("Opción no válida.")
            self._pausa()
    
    def _obtener_datos_gasto(self):
        # (Sin cambios)
        print("\n--- Datos del Gasto ---")
        descripcion = input("Descripción del gasto: ")
        monto_str = input("Monto del gasto (ej: 15000 o 12.5): ")
        if not descripcion.strip() or not monto_str.strip():
            self.mostrar_resultado("Error: La descripción y el monto no pueden estar vacíos.")
            return None, None
        return descripcion, monto_str

    def run_menu_personal(self):
        # (Sin cambios, asumiendo que ya funciona)
        while True:
            self._limpiar_pantalla()
            print("==== MÓDULO DE PERSONAL (GERENTE/ADMIN) ====")
            print("1. Listar todo el personal")
            print("2. Contratar/Actualizar empleado (Asignar Salario/Puesto)")
            print("3. Despedir empleado (Eliminar de DB)")
            print("9. Volver al menú principal")
            opcion = input("Selecciona una opción: ")
            if opcion == '1':
                self.mostrar_resultado(self.personal_vm.listar_personal())
            elif opcion == '2':
                nombre, puesto, salario = self._obtener_datos_empleado()
                if nombre and salario is not None:
                    self.mostrar_resultado(self.personal_vm.contratar_empleado(nombre, puesto, salario))
            elif opcion == '3':
                nombre = input("Nombre del empleado a despedir: ")
                self.mostrar_resultado(self.personal_vm.despedir_empleado(nombre))
            elif opcion == '9':
                break
            else:
                self.mostrar_resultado("Opción no válida.")
            self._pausa()

    def _obtener_datos_empleado(self):
        # (Sin cambios)
        print("\n--- Datos del Empleado ---")
        nombre = input("Nombre (debe coincidir con el registrado): ")
        puesto = input("Puesto (ej: cajero, cocinero): ")
        try:
            salario = float(input("Salario (Mensual): "))
            return nombre, puesto, salario
        except ValueError:
            self.mostrar_resultado("Error: El salario debe ser un número.")
            return None, None, None