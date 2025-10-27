# app/view_model/inventario_vm.py

class InventarioViewModel:
    def __init__(self, inventario_repo):
        self.inventario_repo = inventario_repo

    def _extract(self, item):
        """
        Normaliza distintas formas de item en (id, data_dict).
        Soporta:
         - (id, dict)
         - {'id': id, ...}
         - dict (con 'id' dentro)
        """
        # tupla/lista (id, data)
        if isinstance(item, (list, tuple)) and len(item) == 2:
            pid, data = item
            if isinstance(data, dict):
                return str(pid), dict(data)
            # si data no es dict, intentar convertir
            return str(pid), {"valor": data}

        # dict que incluye 'id'
        if isinstance(item, dict):
            if 'id' in item:
                pid = item.get('id')
                data = dict(item)
                data.pop('id', None)
                return str(pid), data
            # dict sin 'id' -> id = nombre si existe
            nombre = item.get('nombre') or item.get('Nombre') or item.get('producto')
            pid = nombre if nombre else 'N/A'
            return str(pid), dict(item)

        # cualquier otro caso: devolver como valor bruto
        return 'N/A', {"valor": item}

    def _formatear_item(self, doc_id, data):
        if not isinstance(data, dict):
            return f"ID: {doc_id} | Datos no válidos"
        nombre = data.get('nombre') or data.get('Nombre') or data.get('producto') or ''
        cantidad = data.get('cantidad') or data.get('qty') or 0
        costo = data.get('costo') or data.get('precio') or data.get('precio_costo') or 0.0
        try:
            costo_f = float(costo)
        except Exception:
            costo_f = 0.0
        return f"ID: {doc_id} | Nombre: {nombre} | Cantidad: {cantidad} | Costo: ${costo_f:.2f}"

    def listar_inventario(self):
        try:
            inventario = self.inventario_repo.obtener_todo_inventario()
            if not inventario:
                return "Inventario vacío."
            lines = []
            for item in inventario:
                pid, data = self._extract(item)
                lines.append(self._formatear_item(pid, data))
            return "\n".join(lines)
        except Exception as e:
            return f"Error al listar inventario: {e}"

    def buscar_producto(self, nombre):
        try:
            resultados = self.inventario_repo.buscar_producto_por_nombre(nombre)
            if not resultados:
                return f"No se encontraron productos con el nombre '{nombre}'."
            lines = []
            for item in resultados:
                pid, data = self._extract(item)
                lines.append(self._formatear_item(pid, data))
            return "\n".join(lines) if lines else f"No se encontraron productos con el nombre '{nombre}'."
        except Exception as e:
            return f"Error al buscar producto: {e}"

    def agregar_o_actualizar_producto(self, nombre, cantidad_str, precio_str):
        try:
            cantidad = float(cantidad_str)
            precio = float(precio_str)
        except Exception:
            return "Error: Cantidad y Precio deben ser números."
        if not nombre or not str(nombre).strip():
            return "Error: El nombre no puede estar vacío."
        nombre_norm = str(nombre).strip()
        ok = self.inventario_repo.agregar_o_actualizar_producto_por_nombre(nombre_norm, cantidad, precio)
        return f"✅ Producto '{nombre_norm}' agregado/actualizado." if ok else f"❌ No se pudo agregar/actualizar '{nombre_norm}'."

    def eliminar_producto(self, nombre):
        if not nombre or not str(nombre).strip():
            return "Error: El nombre no puede estar vacío."
        ok = self.inventario_repo.eliminar_producto_por_nombre(nombre)
        return f"✅ Producto '{nombre}' eliminado." if ok else f"⚠️ No se encontró '{nombre}'.." 