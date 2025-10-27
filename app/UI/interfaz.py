# app/UI/interfaz.py
import os 
from app.view_model.auth_vm import AuthViewModel
from app.view_model.pedidos_vm import PedidosViewModel
from app.view_model.inventario_vm import InventarioViewModel
from app.view_model.finanzas_vm import FinanzasViewModel
from app.view_model.personal_vm import PersonalViewModel
from app.view_model.ai_vm import AIViewModel
# Asumimos que la clase 'Usuario' está definida en auth_vm.py


class InterfazConsola: 
    
    # Añadido 'ai_vm' al constructor
    def __init__(self, auth_vm, pedidos_vm, inventario_vm, finanzas_vm, personal_vm, ai_vm):
        self.auth_vm = auth_vm
        self.pedidos_vm = pedidos_vm
        self.inventario_vm = inventario_vm
        self.finanzas_vm = finanzas_vm
        self.personal_vm = personal_vm
        self.ai_vm = ai_vm
        
        # Estado de la sesión (self.usuario_actual será un OBJETO Usuario)
        self.usuario_actual = None
        
    # --- UTILIDADES ---
    def _limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear') 

    def _pausa(self):
        input("\nPresiona Enter para continuar...")

    def mostrar_resultado(self, resultado, pausa=True):
        print("\n--- Resultado ---")
        if isinstance(resultado, str):
            print(resultado)
        elif isinstance(resultado, list):
            if not resultado: print("No se encontraron resultados.")
            for item in resultado: print(f"- {item}")
        elif isinstance(resultado, dict):
            if not resultado: print("No se encontraron resultados.")
            for key, value in resultado.items(): print(f"{key}: {value}")
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
                        # auth_vm actualiza self.auth_vm.usuario_actual
                        # Lo copiamos a la interfaz para controlarla
                        self.usuario_actual = self.auth_vm.usuario_actual 
                        self.mostrar_resultado(resultado_login, pausa=True)
                        self.run_menu_principal() # Ir al menú principal
                    else:
                        self.mostrar_resultado(resultado_login, pausa=True)
                        
            elif opcion == '2':
                print("Gracias por usar el sistema. ¡Adiós!")
                break # Rompe el bucle y termina la aplicación
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
            
        # ✅ CORRECCIÓN: Usar .rol (notación de objeto, no .get)
        rol = self.usuario_actual.rol.lower()
        
        if rol == 'administrador':
            self.run_menu_administrador()
        elif rol == 'gerente':
            self.run_menu_gerente()
        else:
            self.run_menu_operativo()
            
    # --- MENÚS SEGÚN ROL ---
    
    def run_menu_administrador(self):
        # ✅ CORRECCIÓN: Usar .nombre (notación de objeto)
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
                self.usuario_actual = None # Limpiar sesión de la UI
                return 
            else:
                self.mostrar_resultado("Opción no válida.", pausa=True)

    def run_menu_gerente(self):
        # ✅ CORRECCIÓN: Usar .nombre (notación de objeto)
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
        # ✅ CORRECCIÓN: Usar .nombre y .rol (notación de objeto)
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
    # (¡Asegúrate de tener tus menús reales aquí!)
    # (Estos son marcadores de posición)
    def run_menu_pedidos(self):
        self.mostrar_resultado("Módulo de Pedidos no implementado.", pausa=True)
    def run_menu_inventario(self):
        self.mostrar_resultado("Módulo de Inventario no implementado.", pausa=True)
    def run_menu_finanzas(self):
        self.mostrar_resultado("Módulo de Finanzas no implementado.", pausa=True)
    def run_menu_personal(self):
        self.mostrar_resultado("Módulo de Personal no implementado.", pausa=True)
    
    
    # --- MENÚ DEL ASISTENTE AI ---
    def _run_menu_asistente(self):
        """
        Inicia la interfaz de chat con el Asistente AI.
        """
        self._limpiar_pantalla()
        
        if not self.ai_vm.is_ready:
            self.mostrar_resultado("El Asistente AI no está disponible. Revisa la GEMINI_API_KEY en tu .env.")
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
            
            # ✅ LÓGICA DE SALIDA
            if pregunta.lower().strip() in ('salir', 'back', 'volver'):
                break # Rompe el bucle del chat y regresa al menú anterior
            
            if not pregunta.strip():
                continue

            # Llama al ViewModel, que inyecta el contexto y pregunta al IA
            respuesta_ia = self.ai_vm.preguntar_al_asistente(pregunta)
            
            # Muestra la respuesta formateada (sin pausa)
            self.mostrar_resultado(respuesta_ia, pausa=False)