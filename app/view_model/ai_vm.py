# app/view_model/ai_vm.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# --- CONFIGURACIÓN DE GEMINI ---
API_KEY = os.environ.get("GEMINI_API_KEY")

_chat_session = None
_is_ai_ready = False # Inicializa como False por defecto

try:
    if API_KEY:
        genai.configure(api_key=API_KEY)
        
        # ✅ MODELO CONFIRMADO: Usamos el que te funcionó
        model = genai.GenerativeModel('gemini-2.5-flash') 
        
        _chat_session = model.start_chat(history=[])
        
        # Establecer _is_ai_ready a True DESPUÉS de una inicialización exitosa
        _is_ai_ready = True 
        print("✅ Asistente AI (Gemini) inicializado correctamente.")
        
    else:
        print("❌ ERROR AI: La clave GEMINI_API_KEY no se encontró en el archivo .env")

except Exception as e:
    print(f"❌ ERROR AI: No se pudo configurar Gemini. Revisa la clave. Detalle: {e}")


class AIViewModel:
    
    # Añadido 'db_repo' para acceder al PERSONAL
    def __init__(self, inventario_repo, finanzas_repo, db_repo):
        """
        Inicializa el VM con los repositorios necesarios para obtener el contexto.
        """
        self.inventario_repo = inventario_repo
        self.finanzas_repo = finanzas_repo
        self.db_repo = db_repo # Repositorio de la DB (para 'usuarios')
        
    @property
    def is_ready(self):
        """ Revisa si el modelo de IA se cargó correctamente. """
        return _is_ai_ready

    def _obtener_contexto_inventario(self):
        """
        Devuelve el inventario en formato JSON para que el IA lo analice.
        """
        if not self.inventario_repo.is_ready: return "Error: Inventario no disponible."
        productos = self.inventario_repo.obtener_todo_inventario()
        if not productos: return "El inventario está vacío."
        productos_limpios = [{k: v for k, v in p.items() if isinstance(v, (str, int, float, bool, list))} for p in productos if isinstance(p, dict)]
        return json.dumps(productos_limpios, indent=2, ensure_ascii=False)

    def _obtener_contexto_finanzas(self):
        """
        Devuelve un resumen de los movimientos (Ventas/Gastos manuales).
        """
        if not self.finanzas_repo.is_ready: return "Error: Finanzas no disponible."
        movimientos = self.finanzas_repo.obtener_todos_los_movimientos()
        if not movimientos: return "No hay movimientos financieros (ventas/gastos manuales)."
        
        balance = sum(mov.get('monto', 0) for mov in movimientos.values())
        resumen = {
            "balance_neto_movimientos_manuales": f"${balance:,.2f}",
            "total_movimientos_registrados": len(movimientos)
        }
        return json.dumps(resumen, indent=2)

    def _obtener_contexto_personal(self):
        """
        Obtiene la lista de personal (empleados) desde la colección 'usuarios'.
        """
        if not self.db_repo.is_ready: return "Error: DB Repo no disponible."
        personal_docs = self.db_repo.obtener_todos_los_documentos('usuarios')
        if not personal_docs: return "No hay personal registrado."
            
        lista_personal = []
        for uid, datos in personal_docs.items():
            if isinstance(datos, dict): 
                lista_personal.append({
                    "nombre": datos.get('nombre', 'N/A'),
                    "rol": datos.get('rol', 'N/A'),
                    "puesto": datos.get('puesto', 'No asignado')
                })
        return json.dumps(lista_personal, indent=2, ensure_ascii=False)


    def preguntar_al_asistente(self, pregunta_usuario: str) -> str:
        """
        Construye el prompt con TODO el contexto y pregunta al modelo.
        """
        if not self.is_ready or not _chat_session:
            return "ERROR: El Asistente AI no está disponible. Revisa tu GEMINI_API_KEY."

        contexto_inventario = self._obtener_contexto_inventario()
        contexto_finanzas = self._obtener_contexto_finanzas()
        contexto_personal = self._obtener_contexto_personal()
        
        # ✅ --- PROMPT DE CONSULTOR DE NEGOCIOS --- ✅
        prompt_completo = f"""
        Actúa como un Consultor de Negocios y Analista de Marketing para un restaurante. 
        Tu trabajo es analizar los datos de contexto proporcionados y responder al gerente.

        REGLAS IMPORTANTES:
        1.  **Análisis de Datos (Objetivo):** Para preguntas sobre hechos (ej: "¿cuántos tomates hay?", "¿quién es el cajero?"), bázate **estrictamente** en los datos de contexto. Si los datos no existen, indícalo.
        2.  **Estrategias (Creativo y Objetivo):** Para preguntas sobre estrategias (ej: "cómo mejorar ventas", "ideas de marketing"), usa tu conocimiento general de negocios para dar sugerencias **objetivas** y **prácticas** que un restaurante pequeño podría implementar.
        3.  **Usa el Contexto como Inspiración:** Si te pido ideas de marketing y ves que el balance financiero es negativo ($-500), sugiere estrategias de bajo costo (ej. redes sociales). Si ves poco stock de 'tomate', sugiere una promoción para productos que no usen tomate.
        4.  **Fuera de Ámbito:** Si la pregunta no tiene relación con el negocio (ej. fútbol, clima), indica amablemente que no tienes esa información, ya que tu enfoque es el restaurante.

        --- DATOS DE CONTEXTO ---
        INVENTARIO (Productos en stock y su costo):
        {contexto_inventario}
        
        FINANZAS (Resumen de movimientos manuales, gastos/ingresos):
        {contexto_finanzas}
        
        PERSONAL (Lista de empleados y sus roles):
        {contexto_personal}
        
        --- PREGUNTA DEL GERENTE ---
        {pregunta_usuario}
        
        --- TU RESPUESTA (Consultor experto y conciso) ---
        """

        try:
            print("...Contactando al Asistente AI...")
            response = _chat_session.send_message(prompt_completo)
            return response.text.strip()
        except Exception as e:
            return f"Error en la comunicación con la API de Gemini: {e}"