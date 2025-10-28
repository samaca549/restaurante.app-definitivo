
class InventarioRepo:
    def __init__(self, db, is_ready):
        self.db = db
        self._is_ready = is_ready

    @property
    def is_ready(self):
        return self._is_ready

    def obtener_todo_inventario(self):
        if not self.is_ready:
            return []
        try:
            docs = self.db.collection('inventario').stream()
            inventario = []
            for doc in docs:
                data = doc.to_dict() or {}
                inventario.append((doc.id, dict(data)))
            return inventario
        except Exception as e:
            print(f"Error en InventarioRepo.obtener_todo_inventario: {e}")
            return []

    def buscar_producto_por_nombre(self, nombre: str):
        if not self.is_ready:
            return []
        try:
            if not nombre or not str(nombre).strip():
                return []
            nombre_lower = str(nombre).lower()
            docs = self.db.collection('inventario').stream()
            resultados = []
            for doc in docs:
                data = doc.to_dict() or {}
                campo_nombre = str(
                    data.get('nombre')
                    or data.get('Nombre')
                    or data.get('producto')
                    or data.get('producto_nombre')
                    or ''
                ).lower()
                if nombre_lower in campo_nombre:
                    resultados.append((doc.id, dict(data)))
            return resultados
        except Exception as e:
            print(f"Error en InventarioRepo.buscar_producto_por_nombre: {e}")
            return []

    def agregar_o_actualizar_producto_por_nombre(self, nombre: str, cantidad: float, costo: float):
        if not self.is_ready:
            return False
        try:
            nombre_clean = str(nombre).strip()
            if not nombre_clean:
                return False

            coleccion = self.db.collection('inventario')
            encontrado_id = None
            for doc in coleccion.stream():
                data = doc.to_dict() or {}
                campo_nombre = str(data.get('nombre') or data.get('Nombre') or '').strip().lower()
                if campo_nombre == nombre_clean.lower():
                    encontrado_id = doc.id
                    break

            payload = {
                'nombre': nombre_clean,
                'cantidad': float(cantidad),
                'costo': float(costo)
            }

            if encontrado_id:
                coleccion.document(encontrado_id).update(payload)
            else:
                coleccion.add(payload)

            return True
        except Exception as e:
            print(f"Error en InventarioRepo.agregar_o_actualizar_producto_por_nombre: {e}")
            return False

    def eliminar_producto_por_nombre(self, nombre: str):
        if not self.is_ready:
            return False
        try:
            nombre_clean = str(nombre).strip()
            if not nombre_clean:
                return False
            coleccion = self.db.collection('inventario')
            removed = 0
            for doc in coleccion.stream():
                data = doc.to_dict() or {}
                campo_nombre = str(data.get('nombre') or data.get('Nombre') or '').strip().lower()
                if campo_nombre == nombre_clean.lower():
                    coleccion.document(doc.id).delete()
                    removed += 1
            return removed > 0
        except Exception as e:
            print(f"Error en InventarioRepo.eliminar_producto_por_nombre: {e}")
            return False
