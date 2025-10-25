# app/view_model/inventario_vm.py

class InventarioViewModel:
    
    def __init__(self, inventario_repo):
        self.inventario_repo = inventario_repo

    def listar_inventario(self):
        """Obtiene y formatea la lista completa del inventario."""
        
        # 1. Verifica el estado del repositorio (usando la lógica de la captura)
        if not self.inventario_repo.is_ready:
            return "Error: Conexión al repositorio de inventario no disponible."

        # 2. Obtiene los productos (línea marcada en la captura)
        productos = self.inventario_repo.obtener_todo_inventario()
        
        # Manejo de caso vacío
        if not productos:
            return "El inventario está vacío."

        # 3. Formatea la respuesta
        respuesta = "==== INVENTARIO ACTUAL ====\n"
        respuesta += f"{'ID':<10}{'Nombre':<30}{'Cantidad':<15}{'Precio/Und':<15}\n"
        respuesta += "-" * 70 + "\n"

        for id_producto, data in productos.items():
            nombre = data.get('nombre', 'N/A')
            cantidad = data.get('cantidad', 0)
            precio_unitario = data.get('precio', 0.0)

            # Formateo de precio con dos decimales y separador de miles
            precio_str = f"${precio_unitario:,.2f}"
            
            respuesta += f"{id_producto:<10}{nombre:<30}{cantidad:<15}{precio_str:<15}\n"

        respuesta += "-" * 70 + "\n"
        return respuesta

    def agregar_producto(self, nombre, cantidad_str, precio_str):
        if not self.inventario_repo.is_ready:
            return "Error: Repositorio de inventario no está listo."
            
        try:
            # Limpieza y conversión de cantidad
            cantidad = int(cantidad_str.strip())
            if cantidad <= 0:
                return "Error: La cantidad debe ser un número entero positivo."

            # Limpieza y conversión de precio (robusto para formatos)
            precio_limpio = precio_str.strip().replace(" ", "") 
            precio_limpio = precio_limpio.replace(".", "").replace(",", ".") # Asume formato latino
            precio = float(precio_limpio)
            
            if precio <= 0:
                return "Error: El precio debe ser un número positivo."

            # Generar ID simple basado en nombre
            id_producto = nombre.lower().replace(' ', '_')
            
            producto_data = {
                "nombre": nombre,
                "cantidad": cantidad,
                "precio": precio
            }

            exito = self.inventario_repo.guardar_producto(id_producto, producto_data)
            
            if exito:
                return f"✅ Producto '{nombre}' agregado/actualizado en inventario."
            else:
                return "Error: No se pudo guardar el producto."

        except ValueError:
            return "Error: La cantidad y el precio deben ser números válidos."
        except Exception as e:
            return f"Error inesperado al agregar producto: {e}"

    def actualizar_stock(self, id_producto, cantidad_nueva_str):
        if not self.inventario_repo.is_ready:
            return "Error: Repositorio de inventario no está listo."
            
        try:
            cantidad_nueva = int(cantidad_nueva_str.strip())
            if cantidad_nueva < 0:
                return "Error: La cantidad no puede ser negativa."

            # El repositorio debe manejar la lógica de actualización en Firebase
            exito = self.inventario_repo.actualizar_stock_producto(id_producto, cantidad_nueva)
            
            if exito:
                return f"✅ Stock de '{id_producto}' actualizado a {cantidad_nueva} unidades."
            else:
                return f"Error: No se pudo actualizar el stock del producto '{id_producto}'. (¿Existe el ID?)"

        except ValueError:
            return "Error: La nueva cantidad debe ser un número entero."
        except Exception as e:
            return f"Error inesperado al actualizar stock: {e}"