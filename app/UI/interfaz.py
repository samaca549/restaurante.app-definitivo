
import os 
from app.view_model.auth_vm import AuthViewModel
from app.view_model.pedidos_vm import PedidosViewModel
from app.view_model.inventario_vm import InventarioViewModel
from app.view_model.finanzas_vm import FinanzasViewModel
from app.view_model.personal_vm import PersonalViewModel
from app.view_model.ai_vm import AIViewModel



class InterfazConsola: 
 
    def __init__(self, auth_vm, pedidos_vm, inventario_vm, finanzas_vm, personal_vm, ai_vm):
        self.auth_vm = auth_vm
        self.pedidos_vm = pedidos_vm
        self.inventario_vm = inventario_vm
        self.finanzas_vm = finanzas_vm
        self.personal_vm = personal_vm
        self.ai_vm = ai_vm
      
        self.usuario_actual = None
        

    def _limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear') 

    def _pausa(self):
        input("\nPresiona Enter para continuar...")

    def mostrar_resultado(self, resultado, pausa=True):
        print("\n--- Resultado ---")
        if isinstance(resultado, str):
            print(resultado)
        elif isinstance(resultado, list):
            if not resultado: 
                print("No se encontraron resultados.")
            for item in resultado: 
                print(f"- {item}")
        elif isinstance(resultado, dict):
            if not resultado: 
                print("No se encontraron resultados.")
            for key, value in resultado.items(): 
                print(f"{key}: {value}")
        else:
            print(str(resultado))
        print("-----------------")
        if pausa:
            self._pausa()

    # --- MENÚ DE INICIO (LOGIN) ---
    def mostrar_menu_inicio(self):
        """ Bucle principal del menú de inicio de sesión. """
        while True:
            self._limpiar_pantalla()
            print("====================================")
            print("==== BIENVENIDO AL SISTEMA RESTAURANTE ====")
            print("====================================")
            print("1. Iniciar Sesión")
            print("2. Salir")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == '1':
                email, password = self._obtener_datos_login() 
                if email and password:
                    resultado_login = self.auth_vm.intentar_login(email, password)
                    
                    if "Login exitoso" in resultado_login:
                        self.usuario_actual = self.auth_vm.usuario_actual 
                        self.mostrar_resultado(resultado_login, pausa=True)
                        self.run_menu_principal() 
                    else:
                        self.mostrar_resultado(resultado_login, pausa=True)
                        
            elif opcion == '2':
                print("Gracias por usar el sistema. ¡Adiós!")
                break 
            else:
                self.mostrar_resultado("Opción no válida.", pausa=True)
                
    def _obtener_datos_login(self):
        self._limpiar_pantalla()
        print("--- INICIO DE SESIÓN ---")
        email = input("Email: ").strip()
        password = input("Contraseña: ").strip()
        return email, password
    
    def _obtener_datos_registro(self):
        self._limpiar_pantalla()
        print("--- REGISTRO DE NUEVO USUARIO (ADMIN) ---")
        email = input("Email: ").strip()
        password = input("Contraseña (mín. 6 caracteres): ").strip()
        nombre = input("Nombre completo: ").strip()
        rol = input("Rol (administrador/gerente/cajero/cocinero): ").lower().strip()
        
        roles_validos = ['administrador', 'gerente', 'cajero', 'cocinero']
        if rol not in roles_validos:
            self.mostrar_resultado(f"Error: Rol no válido. Debe ser uno de: {', '.join(roles_validos)}.")
            return None
        if len(password) < 6:
            self.mostrar_resultado("Error: La contraseña debe tener al menos 6 caracteres.")
            return None
            
        return email, password, nombre, rol

    # --- MENÚ PRINCIPAL (CONTROL DE ROLES) ---
    def run_menu_principal(self):
        if not self.usuario_actual:
            print("Error: No hay usuario logueado.")
            return
            
        rol = self.usuario_actual.rol.lower()
        
        if rol == 'administrador':
            self.run_menu_administrador()
        elif rol == 'gerente':
            self.run_menu_gerente()
        else:
            self.run_menu_operativo()
            
    # --- MENÚS SEGÚN ROL ---
    
    def run_menu_administrador(self):
        nombre = self.usuario_actual.nombre
        while self.usuario_actual:
            self._limpiar_pantalla()
            print(f"Sesión activa: {nombre} (ADMINISTRADOR)")
            print("==== SISTEMA DE GESTIÓN (ADMIN) ====")
            print("1. Módulo de Pedidos")
            print("2. Módulo de Inventario")
            print("3. Módulo de Finanzas")
            print("4. Módulo de Personal")
            print("5. 🛡️ AGREGAR NUEVO USUARIO (ADMIN) 🛡️")
            print("6. 🤖 ASISTENTE AI (Análisis de Datos) 🤖")
            print("9. Cerrar Sesión")
            
            opcion = input("Selecciona una opción: ")

            if opcion == '1': self.run_menu_pedidos()
            elif opcion == '2': self.run_menu_inventario()
            elif opcion == '3': self.run_menu_finanzas()
            elif opcion == '4': self.run_menu_personal()
            elif opcion == '5':
                datos_registro = self._obtener_datos_registro()
                if datos_registro:
                    resultado = self.auth_vm.registrar_usuario_y_rol(*datos_registro) 
                    self.mostrar_resultado(resultado)
            elif opcion == '6': 
                self._run_menu_asistente()
            elif opcion == '9':
                self.auth_vm.cerrar_sesion()
                self.usuario_actual = None 
                return 
            else:
                self.mostrar_resultado("Opción no válida.", pausa=True)

    def run_menu_gerente(self):
        nombre = self.usuario_actual.nombre
        while self.usuario_actual:
            self._limpiar_pantalla()
            print(f"Sesión activa: {nombre} (GERENTE)")
            print("==== SISTEMA DE GESTIÓN (GERENTE) ====")
            print("1. Módulo de Pedidos")
            print("2. Módulo de Inventario")
            print("3. Módulo de Finanzas")
            print("4. Módulo de Personal")
            print("5. 🤖 ASISTENTE AI (Análisis de Datos) 🤖")
            print("9. Cerrar Sesión")
            
            opcion = input("Selecciona una opción: ")

            if opcion == '1': self.run_menu_pedidos()
            elif opcion == '2': self.run_menu_inventario()
            elif opcion == '3': self.run_menu_finanzas()
            elif opcion == '4': self.run_menu_personal()
            elif opcion == '5': 
                self._run_menu_asistente()
            elif opcion == '9':
                self.auth_vm.cerrar_sesion()
                self.usuario_actual = None
                return 
            else:
                self.mostrar_resultado("Opción no válida.", pausa=True)

    def run_menu_operativo(self):
        nombre = self.usuario_actual.nombre
        rol = self.usuario_actual.rol.lower()
        
        while self.usuario_actual:
            self._limpiar_pantalla()
            print(f"Sesión activa: {nombre} ({rol.upper()})")
            print(f"==== MÓDULO {rol.upper()} ====")
            print("1. Módulo de Pedidos")
            if rol == 'cocinero':
                print("2. Módulo de Inventario")
            print("9. Cerrar Sesión")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == '1': self.run_menu_pedidos()
            elif opcion == '2' and rol == 'cocinero': self.run_menu_inventario()
            elif opcion == '9':
                self.auth_vm.cerrar_sesion()
                self.usuario_actual = None
                return
            else:
                self.mostrar_resultado("Opción no válida.", pausa=True)

    # --- MÓDULOS (Pedidos, Inventario, Finanzas, Personal) ---

    def run_menu_pedidos(self):
        """ Muestra el submenú de gestión de pedidos. """
        while True:
            self._limpiar_pantalla()
            print("====================================")
            print("==== MÓDULO DE PEDIDOS ====")
            print("====================================")
            print("1. Listar pedidos activos")
            print("2. Crear nuevo pedido")
            print("3. Marcar pedido como 'Completado'")
            print("4. Marcar pedido como 'Cancelado'")
            print("9. Volver al menú principal")
            print("------------------------------------")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == '1':
                resultado = self.pedidos_vm.listar_pedidos_activos()
                self.mostrar_resultado(resultado, pausa=True)
            elif opcion == '2':
                print("--- Nuevo Pedido ---")
                mesa = input("Mesa: ")
                items_str = input("Items (ej: tomate,papa,arroz): ")
                items = [item.strip() for item in items_str.split(',')]
                resultado = self.pedidos_vm.crear_pedido(mesa, items) 
                self.mostrar_resultado(resultado, pausa=True)
            elif opcion == '3':
                pedido_id = input("ID del pedido a completar: ")
                resultado = self.pedidos_vm.actualizar_estado_pedido(pedido_id, "completado") 
                self.mostrar_resultado(resultado, pausa=True)
            elif opcion == '4':
                pedido_id = input("ID del pedido a cancelar: ")
                resultado = self.pedidos_vm.actualizar_estado_pedido(pedido_id, "cancelado") 
                self.mostrar_resultado(resultado, pausa=True)
            elif opcion == '9':
                break
            else:
                self.mostrar_resultado("Opción no válida.", pausa=True)

    def run_menu_inventario(self):
        """ Muestra el submenú de gestión de inventario. """
        while True:
            self._limpiar_pantalla()
            print("====================================")
            print("==== MÓDULO DE INVENTARIO ====")
            print("====================================")
            print("1. Listar inventario")
            print("2. Buscar producto")
            print("3. Agregar o Actualizar producto")
            print("4. Eliminar producto")
            print("9. Volver al menú principal")
            print("------------------------------------")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == '1':
                resultado = self.inventario_vm.listar_inventario() 
                self.mostrar_resultado(resultado, pausa=True)
            elif opcion == '2':
                nombre = input("Ingresa el nombre (o parte del nombre) a buscar: ")
                resultado = self.inventario_vm.buscar_producto(nombre) 
                self.mostrar_resultado(resultado, pausa=True)
            elif opcion == '3':
                print("--- Agregar/Actualizar Producto ---")
                nombre = input("Nombre del producto: ").strip()
                cantidad_str = input("Cantidad (ej: 10 o 2.5): ").strip()
                precio_str = input("Precio de costo (ej: 1500.50): ").strip()
                resultado = self.inventario_vm.agregar_o_actualizar_producto(nombre, cantidad_str, precio_str) 
                self.mostrar_resultado(resultado, pausa=True)
            elif opcion == '4':
                print("--- Eliminar Producto ---")
                nombre = input("Nombre EXACTO del producto a eliminar: ").strip()
                resultado = self.inventario_vm.eliminar_producto(nombre) 
                self.mostrar_resultado(resultado, pausa=True)
            elif opcion == '9':
                break
            else:
                self.mostrar_resultado("Opción no válida.", pausa=True)

    def run_menu_finanzas(self):
        """ Muestra el submenú de gestión de finanzas. """
        while True:
            self._limpiar_pantalla()
            print("====================================")
            print("==== MÓDULO DE FINANZAS ====")
            print("====================================")
            print("1. Ver balance de movimientos")
            print("2. Registrar gasto manual")
            print("3. Registrar ingreso manual")
            print("9. Volver al menú principal")
            print("------------------------------------")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == '1':
                resultado = self.finanzas_vm.obtener_balance() 
                self.mostrar_resultado(resultado, pausa=True)
            elif opcion == '2':
                print("--- Registrar Gasto ---")
                descripcion = input("Descripción del gasto: ")
                monto_str = input("Monto (ej: 50000): ")
                resultado = self.finanzas_vm.registrar_movimiento(descripcion, monto_str, "gasto") 
                self.mostrar_resultado(resultado, pausa=True)
            elif opcion == '3':
                print("--- Registrar Ingreso ---")
                descripcion = input("Descripción del ingreso: ")
                monto_str = input("Monto (ej: 100000): ")
                resultado = self.finanzas_vm.registrar_movimiento(descripcion, monto_str, "ingreso") 
                self.mostrar_resultado(resultado, pausa=True)
            elif opcion == '9':
                break
            else:
                self.mostrar_resultado("Opción no válida.", pausa=True)

    def run_menu_personal(self):
        """ Muestra el submenú de gestión de personal. """
        while True:
            self._limpiar_pantalla()
            print("====================================")
            print("==== MÓDULO DE PERSONAL ====")
            print("====================================")
            print("1. Listar todo el personal")
            print("2. Eliminar empleado (por email)")
            print("9. Volver al menú principal")
            print("------------------------------------")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == '1':
                resultado = self.personal_vm.listar_personal() 
                self.mostrar_resultado(resultado, pausa=True)
            elif opcion == '2':
                print("--- Eliminar Empleado ---")
                email = input("Email del empleado a eliminar: ").strip()
                confirmacion = input(f"¿Seguro que deseas eliminar a {email}? Esta acción no se puede deshacer. (s/n): ").lower()
                if confirmacion == 's':
                    resultado = self.personal_vm.eliminar_empleado(email) 
                    self.mostrar_resultado(resultado, pausa=True)
                else:
                    self.mostrar_resultado("Eliminación cancelada.", pausa=True)
            elif opcion == '9':
                break
            else:
                self.mostrar_resultado("Opción no válida.", pausa=True)
    
    
    # --- MENÚ DEL ASISTENTE AI ---
    def _run_menu_asistente(self):
        """
        Inicia la interfaz de chat con el Asistente AI.
        """
        self._limpiar_pantalla()
        
        if not self.ai_vm.is_ready:
            self.mostrar_resultado("El Asistente AI no está disponible. Revisa la GEMINI_API_KEY en tu .env.", pausa=True)
            return

        print("======================================================")
        print("====== ASISTENTE DE ANÁLISIS DEL NEGOCIO (Gemini) ======")
        print("======================================================")
        print("Puedo ver Inventario, Finanzas (manuales) y Personal.")
        print("Pregúntame: '¿Cómo mejorar ventas?' o '¿Quién es el cajero?'")
        print("Escribe 'salir' para volver al menú principal.")
        print("-" * 54)
        
        while True:
            pregunta = input("\n[Tú]: ")
            
            if pregunta.lower().strip() in ('salir', 'back', 'volver'):
                break 
            
            if not pregunta.strip():
                continue

            respuesta_ia = self.ai_vm.preguntar_al_asistente(pregunta)
            
            self.mostrar_resultado(respuesta_ia, pausa=False)
