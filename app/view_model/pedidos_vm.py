import pytz
from datetime import datetime


TZ_COLOMBIA = pytz.timezone('America/Bogota')

class PedidosViewModel:
    """
    Clase que gestiona la lógica de negocio relacionada con la toma, 
    gestión y finalización de pedidos.
    Depende de un repositorio de base de datos (db_repo) para interactuar 
    con Firestore/la base de datos.
    """
    def __init__(self, db_repo):
        self.db_repo = db_repo
    
    def obtener_menu(self):
        """
        Obtiene los ítems del menú desde el repositorio y los formatea 
        para una presentación sencilla.
        """
        menu_items = self.db_repo.obtener_menu()
        if not menu_items:

            return {
                "MENU DISPONIBLE (IDs Ficticios)": "Si la colección 'menu' no existe, se usa este placeholder.",
                "1": "Hamburguesa Clásica (12.50 USD)",
                "2": "Pizza Personal (15.00 USD)",
                "3": "Refresco Grande (3.00 USD)"
            }
        
        menu_formato = {}
        for item in menu_items:
            menu_formato[item['id']] = f"{item['nombre']} ({item['precio']} USD)"
        return menu_formato

    def crear_pedido(self, items: list, cajero_uid: str):
        """
        Crea un nuevo pedido en la base de datos con el estado 'ACTIVO'.
        Asegura que el timestamp de creación sea consciente de la zona horaria.
        """
        if not items:
            return "Error: La lista de items está vacía."
            
        total = self._calcular_total_simulado(items)
        
        pedido_data = {
            'items': items,
            'total': total,
            'estado': 'ACTIVO',
            'cajero_uid': cajero_uid,
            'fecha_creacion': datetime.now(TZ_COLOMBIA).isoformat()
        }
        
        pedido_id = self.db_repo.crear_pedido(pedido_data)
        
        if pedido_id:
            return f" Pedido creado con éxito. Total: {total:.2f} USD. ID: {pedido_id}"
        else:
            return " Error al guardar el pedido en la base de datos."

    def ver_pedidos_activos(self):
        """
        Obtiene y formatea la lista de pedidos con estado 'ACTIVO'.
        """
        pedidos = self.db_repo.obtener_pedidos_activos()
        
        if not pedidos:
            return "No hay pedidos activos en este momento."
            
        output = "--- PEDIDOS ACTIVOS ---\n"
  
        for pid, data in sorted(pedidos.items()):
            cajero_identificador = data['cajero_uid'][:4] + '...' 
            output += f"ID: {pid} | Estado: {data['estado']} | Total: {data['total']:.2f} USD | Cajero: {cajero_identificador}\n"
        output += "-----------------------"
        return output

    def finalizar_pedido(self, pedido_id: str):
        """
        Marca un pedido como 'FINALIZADO', simulando el proceso de cobro.
        """
        pedido = self.db_repo.obtener_pedido_por_id(pedido_id)
        
        if not pedido:
            return f"Error: No se encontró el pedido con ID {pedido_id}."
            
        if pedido.get('estado') == 'FINALIZADO':
            return f"El pedido {pedido_id} ya ha sido finalizado y cobrado."


        success = self.db_repo.actualizar_estado_pedido(pedido_id, 'FINALIZADO')
        
        if success:
            return f"✅ Pedido {pedido_id} FINALIZADO y cobrado. Total: {pedido.get('total', 0):.2f} USD."
        else:
            return "❌ Error al actualizar el estado del pedido en la base de datos."
            
    def _calcular_total_simulado(self, items: list) -> float:
        """
        Función auxiliar para calcular el total basado en precios simulados.
        En una aplicación real, se consultaría la base de datos o el menú real.
        """

        precios = {'1': 12.50, '2': 15.00, '3': 3.00}
        total = 0.0
        for item in items:
            item_id = str(item['item_id'])
            cantidad = item['cantidad']
            if item_id in precios:
                total += precios[item_id] * cantidad
        return total
