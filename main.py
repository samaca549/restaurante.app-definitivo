# main.py

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
# Importamos la Interfaz de Consola (Vista)
from app.UI.interfaz import InterfazConsola

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
        
        # ✅ CORRECCIÓN: Pasamos 'auth_repo' y 'db_repo' a PersonalViewModel
        personal_vm = PersonalViewModel(auth_repo, db_repo) 

        # 3. Creamos la Interfaz de Usuario (View)
        ui = InterfazConsola(
            auth_vm,      
            pedidos_vm,   
            inventario_vm, 
            finanzas_vm,  
            personal_vm   
        )

        print("Conexión a Firebase exitosa.")
        ui.mostrar_menu_inicio() 

    except Exception as e:
        print(f"\nERROR FATAL AL INICIAR: No se pudo iniciar la aplicación.")
        print(f"Detalle: {e}")
        print("Verifica si los constructores de los ViewModels y Repositorios están correctos.")

if __name__ == "__main__":
    main()