import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno (al inicio, para Firebase y Gemini)
load_dotenv() 

# Configuración y utilidades
# Aseguramos que la carpeta 'app' esté en la ruta para las importaciones
# Esta línea ya no es necesaria si importamos desde 'app.backend.firebase_init' 
# y la estructura es la que se usa abajo. La elimino para simplificar.
# sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.backend.firebase_init import db, auth_service, is_ready 

# --- Importamos los Repositorios ---
from app.model.data.db_repo import DbRepo
from app.model.data.auth_repo import AuthRepo 
from app.model.data.finanzas_repo import FinanzasRepo 
from app.model.data.inventario_repo import InventarioRepo

# --- Importamos los ViewModels (Lógica) ---
from app.view_model.auth_vm import AuthViewModel 
from app.view_model.pedidos_vm import PedidosViewModel
from app.view_model.inventario_vm import InventarioViewModel
from app.view_model.finanzas_vm import FinanzasViewModel
from app.view_model.personal_vm import PersonalViewModel
from app.view_model.ai_vm import AIViewModel # Importar el VM del AI

# Importamos la Interfaz de Consola (Vista)
from app.UI.interfaz import InterfazConsola # Aseguramos la minúscula 'ui'

def main():
    print("Iniciando la aplicación...")

    if not is_ready:
        print("\n❌ ERROR CRÍTICO: Firebase no se inicializó correctamente.")
        return

    try:
        # 1. Creamos los Repositorios (Conexión a Datos)
        db_repo = DbRepo(db, is_ready)
        auth_repo = AuthRepo(auth_service, is_ready)
        finanzas_repo = FinanzasRepo(db, is_ready) 
        inventario_repo = InventarioRepo(db, is_ready) 

        # 2. Creamos los ViewModels (Lógica de Negocio)
        auth_vm = AuthViewModel(auth_repo, db_repo)
        pedidos_vm = PedidosViewModel(db_repo) 
        inventario_vm = InventarioViewModel(inventario_repo) 
        finanzas_vm = FinanzasViewModel(finanzas_repo) 
        personal_vm = PersonalViewModel(auth_repo, db_repo) 
        
        # Pasamos TODOS los repos de contexto al AI
        ai_vm = AIViewModel(inventario_repo, finanzas_repo, db_repo) 

        # 3. Creamos la Interfaz de Usuario (View)
        # Notar que InterfazConsola ahora recibe 6 argumentos, lo cual es la corrección al error inicial.
        ui = InterfazConsola(
            auth_vm, 	 
            pedidos_vm, 	
            inventario_vm, 
            finanzas_vm, 	
            personal_vm,
            ai_vm # Pasamos el nuevo VM
        )

        print("Conexión a Firebase exitosa.")
        
        # Aviso si el AI no se conectó
        if not ai_vm.is_ready:
            print("⚠️ ADVERTENCIA: Asistente AI no disponible. Revisa GEMINI_API_KEY en .env.")
            
        # Esta línea inicia el menú de login y evita que la app se cierre.
        # Asumo que esta función existe en InterfazConsola
        ui.mostrar_menu_inicio() 

    except Exception as e:
        print(f"\nERROR FATAL AL INICIAR: No se pudo iniciar la aplicación.")
        print(f"Detalle: {e}")

if __name__ == "__main__":
    main()
