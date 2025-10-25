# app/model/data/inventario_repo.py

class InventarioRepo:
    
    def __init__(self, db, is_ready):
        self.db = db
        self._is_ready = is_ready
        
    @property
    def is_ready(self):
        return self._is_ready

    def obtener_todo_inventario(self):
        if not self.is_ready: return []
        try:
            docs = self.db.collection('inventario').stream()
            inventario_list = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                inventario_list.append(data)
            return inventario_list
        except Exception as e:
            print(f"Error en InventarioRepo.obtener_todo_inventario: {e}")
            return []

    def buscar_producto_por_id(self, item_id):
        if not self.is_ready: return None
        try:
            doc_ref = self.db.collection('inventario').document(item_id)
            doc = doc_ref.get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            print(f"Error al buscar producto: {e}")
            return None

    def guardar_o_actualizar_producto(self, item_id, data):
        if not self.is_ready: return False
        try:
            # Usamos .set() para crear o sobrescribir (actualizar)
            self.db.collection('inventario').document(item_id).set(data)
            return True
        except Exception as e:
            print(f"Error al guardar/actualizar producto: {e}")
            return False

    def eliminar_producto(self, item_id):
        if not self.is_ready: return False
        try:
            self.db.collection('inventario').document(item_id).delete()
            return True
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            return False