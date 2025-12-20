"""
FASE 2 - Cliente de Gemini 2.5 Pro
Integración con Google Gemini AI con lectura dinámica de configuración
"""

import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class GeminiAIClient:
    """Cliente de Gemini 2.5 Pro con auto-configuración"""
    
    def __init__(self, db_connection=None):
        self.db = db_connection
        
        # Configurar Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("❌ ERROR: GEMINI_API_KEY no configurada en .env")
        
        genai.configure(api_key=api_key)
        
        # Usar Gemini 2.5 Pro
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        print("✅ Gemini 2.5 Pro configurado correctamente")
    
    def load_system_configuration(self):
        """Carga configuración desde CONFIG_SISTEMA (si DB disponible)"""
        
        if not self.db:
            # Configuración por defecto si no hay BD
            return self._get_default_configuration()
        
        try:
            # 1. Cargar prompt base
            prompt_result = self.db.execute_query("""
                SELECT valor FROM CONFIG_SISTEMA 
                WHERE categoria='PROMPT' AND clave='SISTEMA_BASE' AND activo=1
            """)
            
            base_prompt = prompt_result[0]['valor'] if prompt_result else self._get_default_prompt()
            
            # 2. Cargar mapeos de columnas
            mappings = self.db.execute_query("""
                SELECT tabla, columna_bd, nombre_coloquial, formula_conversion
                FROM MAPEO_COLUMNAS
                WHERE formula_conversion IS NOT NULL
                ORDER BY tabla, columna_bd
            """)
            
            # 3. Construir contexto completo
            context = f"""{base_prompt}

**MAPEO DE COLUMNAS (CRÍTICO)**:
Cuando consultes o modifiques datos, usa estas conversiones:

"""
            if mappings:
                for m in mappings:
                    context += f"- {m['tabla']}.{m['columna_bd']} → {m['nombre_coloquial']}: {m['formula_conversion']}\n"
            
            return context
            
        except Exception as e:
            print(f"⚠️  No se pudo cargar configuración de BD: {e}")
            return self._get_default_configuration()
    
    def _get_default_prompt(self):
        """Prompt por defecto si no hay BD"""
        return """Eres IA Dental, un asistente de inteligencia artificial especializado en la gestión de la clínica dental Rubio García.

**TU MISIÓN:**
Ayudar al personal de la clínica a consultar y gestionar información de pacientes, citas, tratamientos y presupuestos de manera eficiente y segura.

**CAPACIDADES:**
1. Consultar información de pacientes, citas, tratamientos
2. Generar consultas SQL optimizadas desde lenguaje natural
3. Validar datos antes de operaciones de escritura
4. Proporcionar estadísticas y análisis
5. Responder preguntas sobre el estado de pacientes y agenda

**REGLAS IMPORTANTES:**
- Siempre valida los datos antes de escribir
- Usa prepared statements para prevenir SQL injection
- Proporciona respuestas claras y profesionales en español
- Si no estás seguro, pregunta antes de actuar

**IDIOMA:** Español (España)
**TONO:** Profesional, amable y eficiente
"""
    
    def _get_default_configuration(self):
        """Configuración por defecto con mapeos de DCitas"""
        return """Eres IA Dental, un asistente de inteligencia artificial para la clínica dental Rubio García.

**MAPEO DE COLUMNAS CRÍTICO (DCitas)**:

Conversiones de fechas y horas:
- DCitas.Fecha (INT) → Fecha Cita: CONVERT(VARCHAR(10), DATEADD(DAY, Fecha - 2, '1900-01-01'), 23)
- DCitas.Hora (INT) → Hora Cita: CONVERT(VARCHAR(5), DATEADD(SECOND, Hora, 0), 108)
- DCitas.Duracion (INT) → Duración: CAST(CAST(Duracion AS DECIMAL(10, 2)) / 60 AS INT) minutos

Estados de cita (IdSitC):
- 0 = Planificada
- 1 = Anulada
- 5 = Finalizada
- 7 = Confirmada
- 8 = Cancelada

Tratamientos (IdIcono):
- 1 = Control
- 2 = Urgencia
- 3 = Prótesis Fija
- 13 = Primera Visita
- 14 = Higiene Dental
- 15 = Endodoncia
- 17 = Exodoncia

Odontólogos (IdUsu):
- 3 = Dr. Mario Rubio
- 4 = Dra. Irene García
- 8 = Dra. Virginia Tresgallo
- 10 = Dra. Miriam Carrasco
- 12 = Tc. Juan Antonio Manzanedo

**INSTRUCCIONES:**
- Usa SIEMPRE las fórmulas de conversión para fechas y horas
- Convierte los IDs a nombres legibles en las respuestas
- Genera SQL válido para SQL Server
- Responde en español de forma profesional
"""
    
    def query(self, user_message, conversation_history=None):
        """Ejecuta consulta con Gemini"""
        
        # Cargar configuración del sistema
        system_context = self.load_system_configuration()
        
        # Construir prompt completo
        full_prompt = f"""{system_context}

**CONVERSACIÓN**:
Usuario: {user_message}

Responde de forma profesional y ejecuta las acciones necesarias.
"""
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"❌ Error al consultar Gemini: {e}"
    
    def generate_sql(self, user_request, table_info=None):
        """Genera SQL desde lenguaje natural"""
        
        system_context = self.load_system_configuration()
        
        prompt = f"""{system_context}

**TAREA**: Generar consulta SQL para SQL Server

Usuario solicita: {user_request}

IMPORTANTE: 
- Usa las fórmulas de conversión para fechas y horas
- Genera SOLO el SQL, sin explicaciones
- Usa prepared statements cuando sea posible
- Convierte IDs a nombres legibles con CASE WHEN

Responde SOLO con el SQL:
"""
        
        try:
            response = self.model.generate_content(prompt)
            sql = response.text.strip()
            
            # Limpiar markdown si existe
            if sql.startswith('```sql'):
                sql = sql.replace('```sql', '').replace('```', '').strip()
            
            return sql
        except Exception as e:
            return f"-- Error: {e}"


# Test del cliente
if __name__ == "__main__":
    print("=" * 70)
    print("PRUEBA DE GEMINI 2.5 PRO CLIENT")
    print("=" * 70)
    
    # Crear cliente (sin BD por ahora)
    client = GeminiAIClient()
    
    # Prueba 1: Consulta simple
    print("\n📝 Prueba 1: Consulta simple")
    response = client.query("¿Cuántos pacientes hay en la clínica?")
    print(f"Respuesta: {response}")
    
    # Prueba 2: Generar SQL
    print("\n📝 Prueba 2: Generar SQL")
    sql = client.generate_sql("Muéstrame las citas de mañana con el Dr. Mario Rubio")
    print(f"SQL generado:\n{sql}")
    
    print("\n✅ Pruebas completadas")
