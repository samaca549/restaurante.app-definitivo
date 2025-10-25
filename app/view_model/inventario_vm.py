# app/view_model/inventario_vm.py
import math

class InventarioViewModel:
    
    def __init__(self, inventario_repo):
        self.inventario_repo = inventario_repo
        
    def listar_inventario(self):
        if not self.inventario_repo.is_ready:
            return "Error: Conexión al repositorio de inventario no disponible."
            
        productos = self.inventario_repo.obtener_todo_inventario()
        
        if not productos:
            return "El inventario está vacío."
            
        respuesta = "==== INVENTARIO ACTUAL ====\n"
        respuesta += f"{'ID':<20}{'Nombre':<30}{'Cantidad':<15}{'Precio Costo':<15}\n"
        respuesta += "-" * 80 + "\n"
        
        for prod in productos:
            nombre = prod.get('nombre', 'N/A')
            cantidad = prod.get('cantidad', 0)
            precio = prod.get('precio', 0.0)
            item_id = prod.get('id', 'N/A')
            
            try:
                cant_str = str(int(cantidad)) if (isinstance(cantidad, (int, float)) and cantidad == math.floor(cantidad)) else f"{cantidad:.2f}"
                precio_str = f"${precio:,.2f}"
            except Exception:
                cant_str = str(cantidad)
                precio_str = f"${precio}"

            respuesta += f"{item_id:<20}{nombre:<30}{cant_str:<15}{precio_str:<15}\n"
            
        return respuesta

    def buscar_producto(self, nombre_parcial):
        if not self.inventario_repo.is_ready:
            return "Error: Repositorio no disponible."
            
        productos = self.inventario_repo.obtener_todo_inventario()
        resultados = []
        nombre_buscado = nombre_parcial.lower()
        
        for prod in productos:
            if nombre_buscado in prod.get('nombre', '').lower():
                resultados.append(prod)
                
        if not resultados:
            return f"No se encontraron productos con el nombre '{nombre_parcial}'."

        respuesta = f"==== RESULTADOS PARA '{nombre_parcial.upper()}' ====\n"
        for prod in resultados:
            respuesta += f"- ID: {prod.get('id')}, Nombre: {prod.get('nombre')}, Cantidad: {prod.get('cantidad')}, Precio Costo: ${prod.get('precio'):,.2f}"
            
        return respuesta

    def agregar_o_actualizar_producto(self, nombre, cantidad, precio):
        if not self.inventario_repo.is_ready:
            return "Error: Repositorio no disponible."
        if not nombre or cantidad is None or precio is None:
            return "Error: Todos los campos son obligatorios."

        # El ID será el nombre en minúsculas y con guiones bajos
        item_id = nombre.lower().replace(" ", "_").strip()
        if not item_id:
             return "Error: Nombre de producto inválido."

        data = {
            'nombre': nombre,
            'cantidad': float(cantidad), 
            'precio': float(precio) # Precio de costo
        }
        
        producto_existente = self.inventario_repo.buscar_producto_por_id(item_id)
        
        if self.inventario_repo.guardar_o_actualizar_producto(item_id, data):
            accion = "actualizado" if producto_existente else "agregado"
            return f"Producto '{nombre}' {accion} con éxito. (ID: {item_id})"
        else:
            return f"Error al guardar el producto '{nombre}'."

    def eliminar_producto(self, nombre):
        if not self.inventario_repo.is_ready:
            return "Error: Repositorio no disponible."
        if not nombre:
            return "Error: Debe proporcionar un nombre."
            
        item_id = nombre.lower().replace(" ", "_").strip()
        
        if not self.inventario_repo.buscar_producto_por_id(item_id):
            return f"Error: No se encontró un producto con ID '{item_id}' (Nombre: {nombre})."
        
        if self.inventario_repo.eliminar_producto(item_id):
            return f"Producto '{nombre}' eliminado con éxito (ID: {item_id})."
        else:
            return f"Error: No se pudo eliminar el producto '{nombre}'."