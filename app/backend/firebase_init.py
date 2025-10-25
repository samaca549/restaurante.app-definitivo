import firebase_admin
from firebase_admin import credentials, firestore, auth
import os

CRED_PATH = 'serviceAccountKey.json' 
DATABASE_URL = "https://TU_PROYECTO_ID.firebaseio.com" 

db = None
auth_service = None 
is_ready = False 

def inicializar_firebase():
    global db, auth_service, is_ready
    
    if firebase_admin._apps:
        try:
            db = firestore.client()
            auth_service = auth
            is_ready = True
            return
        except Exception:
            pass

    try:
        if not os.path.exists(CRED_PATH):
            raise FileNotFoundError(f"El archivo de credenciales '{CRED_PATH}' no se encontró.")

        cred = credentials.Certificate(CRED_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': DATABASE_URL
        })

        db = firestore.client()
        auth_service = auth
        is_ready = True
        
        print("✅ Conexión con Firebase establecida. Clientes de Auth y Firestore listos.")

    except FileNotFoundError as e:
        print(f"\n❌ ERROR CRÍTICO DE CONFIGURACIÓN: {e}")
        print("Asegúrate de tener el archivo 'serviceAccountKey.json' en la raíz del proyecto.")
        is_ready = False
    except Exception as e:
        print(f"\n❌ ERROR FATAL AL INICIAR: No se pudo conectar a Firebase.")
        print(f"Detalle: {e}")
        print("Verifica si el ID de proyecto en DATABASE_URL es correcto.")
        is_ready = False
        
inicializar_firebase()