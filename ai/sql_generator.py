"""
FASE 2/3 - Generador de SQL con Gemini
Genera consultas SQL desde lenguaje natural con validación
"""

import re
from gemini_client import GeminiAIClient


class SQLGenerator:
    """Generador de SQL usando Gemini con validación"""
    
    def __init__(self, gemini_client, db_connection=None):
        self.gemini = gemini_client
        self.db = db_connection
        self.dangerous_keywords = ['DROP', 'TRUNCATE', 'DELETE FROM', 'ALTER TABLE', 'EXEC']
    
    def generate_sql(self, user_request, allow_write=False):
        """Genera SQL desde lenguaje natural"""
        
        print(f"🤖 Generando SQL para: {user_request}")
        
        # Generar SQL con Gemini
        sql = self.gemini.generate_sql(user_request)
        
        # Validar SQL
        validated_sql = self.validate_sql(sql, allow_write)
        
        return validated_sql
    
    def validate_sql(self, sql, allow_write=False):
        """Valida que el SQL sea seguro"""
        
        if not sql or sql.startswith('--'):
            raise ValueError("No se pudo generar SQL válido")
        
        sql_upper = sql.upper()
        
        # Prevenir operaciones peligrosas
        for keyword in self.dangerous_keywords:
            if keyword in sql_upper:
                raise ValueError(f"❌ SQL contiene operación peligrosa: {keyword}")
        
        # Si no se permiten escrituras, solo SELECT
        if not allow_write:
            if not sql_upper.strip().startswith('SELECT'):
                raise ValueError("❌ Solo se permiten consultas SELECT en modo lectura")
        
        # Validar que no haya múltiples statements (prevenir SQL injection)
        if ';' in sql and not sql.strip().endswith(';'):
            raise ValueError("❌ No se permiten múltiples statements SQL")
        
        print("✅ SQL validado correctamente")
        return sql
    
    def execute_sql(self, sql, params=None):
        """Ejecuta SQL validado en la base de datos"""
        
        if not self.db:
            return {"error": "Base de datos no disponible"}
        
        try:
            result = self.db.execute_query(sql, params)
            return {
                "success": True,
                "rows": result,
                "count": len(result) if result else 0
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def natural_language_query(self, user_request, execute=False):
        """Procesa consulta en lenguaje natural completa"""
        
        try:
            # 1. Generar SQL
            sql = self.generate_sql(user_request, allow_write=False)
            
            result = {
                "request": user_request,
                "sql": sql,
                "executed": False
            }
            
            # 2. Ejecutar si se solicita
            if execute and self.db:
                execution_result = self.execute_sql(sql)
                result.update(execution_result)
                result["executed"] = True
            
            return result
            
        except Exception as e:
            return {
                "request": user_request,
                "error": str(e),
                "executed": False
            }


# Test del generador
if __name__ == "__main__":
    print("=" * 70)
    print("PRUEBA DE SQL GENERATOR")
    print("=" * 70)
    
    # Crear cliente Gemini
    gemini = GeminiAIClient()
    
    # Crear generador
    generator = SQLGenerator(gemini)
    
    # Pruebas
    test_queries = [
        "Muéstrame todas las citas de mañana",
        "¿Cuántos pacientes tenemos activos?",
        "Lista los tratamientos del paciente Juan Pérez",
        "Muéstrame las citas confirmadas de esta semana con la Dra. García"
    ]
    
    for query in test_queries:
        print(f"\n📝 Consulta: {query}")
        result = generator.natural_language_query(query, execute=False)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ SQL generado:\n{result['sql']}\n")
    
    # Prueba de validación
    print("\n🔒 Prueba de validación de seguridad:")
    try:
        dangerous_sql = "DROP TABLE Pacientes"
        generator.validate_sql(dangerous_sql)
    except ValueError as e:
        print(f"✅ Validación funcionó: {e}")
    
    print("\n✅ Pruebas completadas")
