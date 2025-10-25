# app/view_model/finanzas_vm.py
import datetime
try:
    from zoneinfo import ZoneInfo
    TZ_COLOMBIA = ZoneInfo("America/Bogota")
except ImportError:
    # Fallback para Python < 3.9
    TZ_COLOMBIA = datetime.timezone(datetime.timedelta(hours=-5), name="America/Bogota")

# Helper class
class MovimientoFinanciero:
    def __init__(self, id_mov, tipo, descripcion, monto, fecha_hora):
        self.id = id_mov
        self.tipo = tipo
        self.descripcion = descripcion
        self.monto = monto
        self.fecha_hora = fecha_hora
    
    def a_diccionario(self):
        return {
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "monto": self.monto,
            "fecha_hora": self.fecha_hora # ISO string format
        }

class FinanzasViewModel:
    
    def __init__(self, finanzas_repo):
        self.finanzas_repo = finanzas_repo 

    def calcular_ingresos_del_dia(self):
        if not self.finanzas_repo.is_ready:
            return "Error: Repositorio de finanzas no está listo."
        
        try:
            hoy = datetime.datetime.now(TZ_COLOMBIA).date()
            pedidos = self.finanzas_repo.obtener_pedidos_para_reporte() 
            ingresos_totales = 0.0
            
            for pedido in pedidos:
                fecha_str = pedido.get('fecha_finalizacion') # Buscamos la fecha de finalización
                total = pedido.get('total', 0.0)
                estado = pedido.get('estado', 'ACTIVO').upper()

                if estado != 'FINALIZADO' or not fecha_str:
                    continue # Ignoramos pedidos no finalizados

                try:
                    if isinstance(fecha_str, str):
                        # Manejo de formatos ISO/Zoulou
                        fecha_pedido = datetime.datetime.fromisoformat(fecha_str.replace('Z', '+00:00')).date()
                    elif hasattr(fecha_str, 'date'): # Si es un Timestamp de Firebase
                        fecha_pedido = fecha_str.astimezone(TZ_COLOMBIA).date()
                    else:
                        continue
                except Exception:
                    continue 
                
                if fecha_pedido == hoy:
                    ingresos_totales += float(total) 

            if ingresos_totales == 0.0:
                return f"No se registraron ingresos (pedidos finalizados) en la fecha {hoy.isoformat()}."
            
            # ✅ CORRECCIÓN 1: Formato f-string usando :,.2f
            return f"Ingresos totales del día ({hoy.isoformat()}): ${ingresos_totales:,.2f}"
        
        except Exception as e:
            return f"Error al calcular ingresos: {e}"


    def obtener_reporte_gastos(self):
        movimientos = self.finanzas_repo.obtener_todos_los_movimientos()
        
        if not movimientos:
            return "No hay movimientos financieros (gastos o ingresos manuales) registrados."
            
        respuesta = "==== REPORTE DE GASTOS Y MOVIMIENTOS ====\n"
        respuesta += f"{'Fecha':<20}{'Tipo':<10}{'Monto':<15}{'Descripción':<40}\n"
        respuesta += "-" * 85 + "\n"
        
        balance_parcial = 0.0
        
        # Ordenamos por fecha de forma descendente
        for id_mov, detalles in sorted(movimientos.items(), key=lambda item: item[1].get('fecha_hora', ''), reverse=True):
            tipo = detalles.get('tipo', 'N/A').upper()
            monto = detalles.get('monto', 0.0)
            descripcion = detalles.get('descripcion', 'Sin descripción')
            fecha_hora_str = detalles.get('fecha_hora', '')
            
            fecha_str = fecha_hora_str[:16].replace('T', ' ') if fecha_hora_str else 'N/A'
            balance_parcial += monto 
            
            # ✅ CORRECCIÓN 2: Asegurar formato :,.2f para monto en el reporte de gastos
            monto_str = f"${monto:,.2f}"
            if tipo == 'EGRESO':
                monto_str = f"(${abs(monto):,.2f})" # Paréntesis para negativo
            
            respuesta += f"{fecha_str:<20}{tipo:<10}{monto_str:<15}{descripcion:<40}\n"
            
        respuesta += "-" * 85 + "\n"
        # ✅ CORRECCIÓN 3: Asegurar formato :,.2f para balance neto
        respuesta += f"BALANCE NETO (Movimientos Manuales): ${balance_parcial:,.2f}"
        return respuesta

    
    def registrar_gasto(self, descripcion, monto_str):
        return self.registrar_movimiento(tipo="egreso", 
                                         descripcion=descripcion, 
                                         monto_str=monto_str)

    def registrar_movimiento(self, tipo, descripcion, monto_str):
        if not self.finanzas_repo.is_ready:
            return "Error: Repositorio de finanzas no está listo."
            
        try:
            # ✅ CORRECCIÓN 4: Limpieza robusta de la cadena de monto para aceptar 1.000,50 o 1,000.50
            
            # 1. Elimina espacios en blanco
            monto_limpio = monto_str.strip().replace(" ", "") 
            
            # 2. Si hay coma y punto, asumimos formato latino (punto miles, coma decimal)
            if monto_limpio.count('.') > 0 and monto_limpio.count(',') > 0 and monto_limpio.rfind(',') > monto_limpio.rfind('.'):
                # Ejemplo: 1.000,50 -> 1000.50
                monto_limpio = monto_limpio.replace(".", "").replace(",", ".")
            else:
                 # Asumimos que la coma es de miles (1,000.50) o que el punto es decimal (10.50)
                monto_limpio = monto_limpio.replace(",", "")
            
            monto_num = float(monto_limpio)
            
            if monto_num <= 0:
                return "Error: El monto debe ser un número positivo."
            
            monto_final = -monto_num if tipo == "egreso" else monto_num
            fecha_hora = datetime.datetime.now(TZ_COLOMBIA).isoformat()
            # Generar un ID único basado en tiempo
            id_mov = f"MOV-{datetime.datetime.now().timestamp()}"
            mov = MovimientoFinanciero(id_mov, tipo, descripcion, monto_final, fecha_hora)
            
            exito = self.finanzas_repo.guardar_movimiento(id_mov, mov.a_diccionario())
            
            if exito:
                return f"Movimiento '{tipo.upper()}' registrado por ${abs(monto_num):,.2f}"
            else:
                return "Error: No se pudo guardar el movimiento."

        except ValueError:
            return f"Error: El monto '{monto_str}' no es un número válido."
        except Exception as e:
            return f"Error inesperado al registrar movimiento: {e}"