# app/model/data/finanzas_repo.py
import datetime
from firebase_admin import firestore

class FinanzasRepo:
    
    def __init__(self, db, is_ready):
        self.db = db
        self._is_ready = is_ready
        
    @property
    def is_ready(self):
        return self._is_ready

    # --- Gestión de Gastos (MOVIMIENTOS) ---

    def guardar_movimiento(self, id_mov: str, data: dict) -> bool:
        if not self.is_ready: return False
        try:
            self.db.collection('movimientos').document(id_mov).set(data)
            return True
        except Exception as e:
            print(f"Error al guardar movimiento financiero {id_mov}: {e}")
            return False

    def obtener_todos_los_movimientos(self) -> dict:
        if not self.is_ready: return {}
        try:
            # Obtenemos todos los movimientos ordenados
            docs = self.db.collection('movimientos').order_by('fecha_hora', direction=firestore.Query.DESCENDING).stream()
            return {doc.id: doc.to_dict() for doc in docs}
        except Exception as e:
            print(f"Error al obtener movimientos financieros: {e}")
            return {}

    # --- Gestión de Pedidos (INGRESOS) ---

    def obtener_pedidos_para_reporte(self) -> list:
        if not self.is_ready: return []
        try:
            # Obtenemos todos los pedidos
            query = self.db.collection('pedidos').stream()
            return [doc.to_dict() for doc in query]
        except Exception as e:
            print(f"Error al obtener pedidos para reporte de ingresos: {e}")
            return []