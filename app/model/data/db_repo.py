# app/model/data/db_repo.py

from firebase_admin import firestore

class DbRepo:
    
    def __init__(self, db_client: firestore.client, is_ready_status: bool):
        self.db = db_client
        self._is_ready = is_ready_status 
        
        if not self.is_ready:
            print("❌ ATENCIÓN: DbRepo inicializado, pero la conexión a Firestore no está lista.")

    @property
    def is_ready(self):
        return self._is_ready


    def obtener_datos_usuario(self, uid: str) -> tuple[str | None, str | None]:
        if not self.is_ready: return None, None
        try:
            doc_ref = self.db.collection('usuarios').document(uid).get()
            if doc_ref.exists:
                data = doc_ref.to_dict()
                return data.get('rol'), data.get('nombre')
            return None, None
        except Exception as e:
            print(f"ERROR DB: Fallo al obtener datos de usuario {uid}: {e}")
            return None, None

    def crear_registro_usuario(self, uid: str, email: str, nombre: str, rol: str) -> bool:
        if not self.is_ready: return False
        try:
            doc_ref = self.db.collection('usuarios').document(uid)
            doc_ref.set({
                'nombre': nombre,
                'rol': rol,
                'email': email,
                'salario': 0.0, # Salario inicial
                'puesto': rol # Puesto inicial
            })
            return True
        except Exception as e:
            print(f"ERROR DB: Fallo al crear registro de usuario {uid}: {e}")
            return False

    def obtener_todos_los_documentos(self, collection_name: str) -> dict | None:
        if not self.is_ready: return None
        try:
            docs = self.db.collection(collection_name).stream()
            return {doc.id: doc.to_dict() for doc in docs}
        except Exception as e:
            print(f"ERROR DB: Fallo al obtener todos los documentos de {collection_name}: {e}")
            return None

    def actualizar_documento(self, collection_name: str, doc_id: str, data: dict) -> bool:
        if not self.is_ready: return False
        try:
            self.db.collection(collection_name).document(doc_id).set(data, merge=True)
            return True
        except Exception as e:
            print(f"ERROR DB: Fallo al actualizar documento {doc_id}: {e}")
            return False

    def eliminar_documento(self, collection_name: str, doc_id: str) -> bool:
        if not self.is_ready: return False
        try:
            self.db.collection(collection_name).document(doc_id).delete()
            return True
        except Exception as e:
            print(f"ERROR DB: Fallo al eliminar documento {doc_id}: {e}")
            return False


    def obtener_menu(self):
        if not self.is_ready: return []
        try:
            docs = self.db.collection('menu').stream()
            menu = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id 
                menu.append(data)
            return menu
        except Exception as e:
            print(f"ERROR DB: Fallo al obtener el menú: {e}")
            return []

    def crear_pedido(self, pedido_data: dict) -> str | None:
        if not self.is_ready: return None
        try:
            timestamp, doc_ref = self.db.collection('pedidos').add(pedido_data)
            return doc_ref.id
        except Exception as e:
            print(f"ERROR DB: Fallo al crear pedido: {e}")
            return None

    def obtener_pedidos_activos(self):
        if not self.is_ready: return {}
        try:
            query = self.db.collection('pedidos').where('estado', '==', 'ACTIVO').stream()
            return {doc.id: doc.to_dict() for doc in query}
        except Exception as e:
            print(f"ERROR DB: Fallo al obtener pedidos activos: {e}")
            return {}
            
    def obtener_pedido_por_id(self, pedido_id: str):
        if not self.is_ready: return None
        try:
            doc_ref = self.db.collection('pedidos').document(pedido_id).get()
            return doc_ref.to_dict() if doc_ref.exists else None
        except Exception as e:
            print(f"ERROR DB: Fallo al obtener pedido {pedido_id}: {e}")
            return None

    def actualizar_estado_pedido(self, pedido_id: str, nuevo_estado: str, fecha_iso: str = None):
        if not self.is_ready: return False
        try:
            doc_ref = self.db.collection('pedidos').document(pedido_id)
            update_data = {'estado': nuevo_estado}
            
            if nuevo_estado == 'FINALIZADO' and fecha_iso:
                update_data['fecha_finalizacion'] = fecha_iso
                
            doc_ref.update(update_data)
            return True
        except Exception as e:
            print(f"ERROR DB: Fallo al actualizar estado del pedido {pedido_id}: {e}")
            return False
