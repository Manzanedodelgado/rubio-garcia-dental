"""
FASE 1 - Poblador de CONFIG_SISTEMA
Lee los resultados del auto-descubrimiento y popula la tabla CONFIG_SISTEMA
"""

import json
from db_connection import DatabaseConnection


class ConfigSystemPopulator:
    """Popula la tabla CONFIG_SISTEMA con la configuración inicial"""
    
    def __init__(self, db_connection, discovery_file='database/schema/auto_discovery_results.json'):
        self.db = db_connection
        
        # Cargar resultados del auto-descubrimiento
        with open(discovery_file, 'r', encoding='utf-8') as f:
            self.discovery = json.load(f)
    
    def create_config_table(self):
        """Crea la tabla CONFIG_SISTEMA si no existe"""
        print("📋 Creando tabla CONFIG_SISTEMA...")
        
        # Leer y ejecutar el script SQL
        with open('database/schema/CONFIG_SISTEMA.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Ejecutar cada statement (separados por GO)
        statements = sql_script.split('GO')
        
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    self.db.execute_query(statement)
                except Exception as e:
                    # Ignorar errores de tabla ya existente
                    if 'already exists' not in str(e):
                        print(f"⚠️  {e}")
        
        print("✅ Tabla CONFIG_SISTEMA lista")
    
    def insert_system_prompt(self):
        """Inserta el prompt del sistema"""
        print("💬 Insertando prompt del sistema...")
        
        query = """
        INSERT INTO CONFIG_SISTEMA 
        (categoria, clave, valor, tipo_dato, prioridad, modificado_por, razon_cambio)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        self.db.execute_query(query, [
            'PROMPT',
            'SISTEMA_BASE',
            self.discovery['system_prompt'],
            'TEXT',
            1,  # Máxima prioridad
            'AUTO_DESCUBRIMIENTO',
            'Prompt inicial generado automáticamente por análisis de esquema'
        ])
        
        print("✅ Prompt del sistema insertado")
    
    def insert_business_rules(self):
        """Inserta las reglas de negocio deducidas"""
        print(f"📜 Insertando {len(self.discovery['business_rules'])} reglas de negocio...")
        
        query = """
        INSERT INTO CONFIG_SISTEMA 
        (categoria, clave, valor, tipo_dato, prioridad, modificado_por, razon_cambio)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        inserted = 0
        for i, rule in enumerate(self.discovery['business_rules']):
            # Generar clave única para la regla
            rule_key = f"{rule['type']}_{rule.get('table', 'GLOBAL')}_{rule.get('column', 'GENERAL')}_{i}"
            
            # Convertir regla a JSON
            rule_json = json.dumps(rule, ensure_ascii=False)
            
            # Determinar prioridad basada en tipo de regla
            priority = self._get_rule_priority(rule['type'])
            
            try:
                self.db.execute_query(query, [
                    'REGLA_NEGOCIO',
                    rule_key,
                    rule_json,
                    'JSON',
                    priority,
                    'AUTO_DESCUBRIMIENTO',
                    f"Regla deducida automáticamente: {rule['type']}"
                ])
                inserted += 1
            except Exception as e:
                print(f"⚠️  Error insertando regla {rule_key}: {e}")
        
        print(f"✅ {inserted} reglas de negocio insertadas")
    
    def insert_table_descriptions(self):
        """Inserta las descripciones de tablas"""
        print(f"📊 Insertando descripciones de {len(self.discovery['table_descriptions'])} tablas...")
        
        query = """
        INSERT INTO CONFIG_SISTEMA 
        (categoria, clave, valor, tipo_dato, prioridad, modificado_por, razon_cambio)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        for table_name, description in self.discovery['table_descriptions'].items():
            try:
                self.db.execute_query(query, [
                    'DESCRIPCION_TABLA',
                    table_name,
                    description,
                    'TEXT',
                    50,
                    'AUTO_DESCUBRIMIENTO',
                    'Descripción deducida automáticamente'
                ])
            except Exception as e:
                print(f"⚠️  Error insertando descripción de {table_name}: {e}")
        
        print("✅ Descripciones de tablas insertadas")
    
    def insert_metadata(self):
        """Inserta metadatos del sistema"""
        print("⚙️  Insertando metadatos del sistema...")
        
        query = """
        INSERT INTO CONFIG_SISTEMA 
        (categoria, clave, valor, tipo_dato, prioridad, modificado_por, razon_cambio)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        metadata = [
            ('CONFIGURACION', 'VERSION_SISTEMA', '1.0.0', 'TEXT', 10, 'SISTEMA', 'Versión inicial'),
            ('CONFIGURACION', 'FECHA_INICIALIZACION', self.discovery['metadata']['discovered_at'], 'TEXT', 10, 'SISTEMA', 'Fecha de inicialización'),
            ('CONFIGURACION', 'TOTAL_TABLAS', str(self.discovery['metadata']['total_tables_analyzed']), 'NUMBER', 10, 'SISTEMA', 'Total de tablas analizadas'),
            ('CONFIGURACION', 'TOTAL_REGLAS', str(self.discovery['metadata']['total_rules']), 'NUMBER', 10, 'SISTEMA', 'Total de reglas deducidas'),
            ('CONFIGURACION', 'MODO_ESCRITURA', 'false', 'BOOLEAN', 5, 'SISTEMA', 'Modo de escritura desactivado por seguridad'),
            ('CONFIGURACION', 'IDIOMA', 'es-ES', 'TEXT', 10, 'SISTEMA', 'Idioma del sistema'),
        ]
        
        for config in metadata:
            try:
                self.db.execute_query(query, list(config))
            except Exception as e:
                print(f"⚠️  Error insertando metadata: {e}")
        
        print("✅ Metadatos insertados")
    
    def _get_rule_priority(self, rule_type):
        """Determina la prioridad de una regla según su tipo"""
        priorities = {
            'INTEGRIDAD_REFERENCIAL': 10,
            'CAMPO_OBLIGATORIO': 20,
            'UNICIDAD': 30,
            'VALIDACION_CHECK': 40,
            'VALIDACION_CONTABLE': 50,
            'VALIDACION_TEMPORAL': 60,
            'VALIDACION_FORMATO': 70,
            'MAQUINA_ESTADOS': 80,
        }
        return priorities.get(rule_type, 100)
    
    def populate_all(self):
        """Ejecuta el proceso completo de población"""
        print("=" * 70)
        print("POBLANDO CONFIG_SISTEMA")
        print("=" * 70)
        
        # Crear tabla
        self.create_config_table()
        
        # Insertar datos
        self.insert_system_prompt()
        self.insert_business_rules()
        self.insert_table_descriptions()
        self.insert_metadata()
        
        # Verificar
        result = self.db.execute_query("SELECT COUNT(*) as total FROM CONFIG_SISTEMA")
        total = result[0]['total']
        
        print("\n" + "=" * 70)
        print(f"✅ POBLACIÓN COMPLETADA: {total} registros en CONFIG_SISTEMA")
        print("=" * 70)
        
        return total
    
    def show_summary(self):
        """Muestra un resumen de la configuración"""
        print("\n📊 RESUMEN DE CONFIG_SISTEMA:")
        
        # Contar por categoría
        query = """
        SELECT categoria, COUNT(*) as total, SUM(CASE WHEN activo=1 THEN 1 ELSE 0 END) as activos
        FROM CONFIG_SISTEMA
        GROUP BY categoria
        ORDER BY total DESC
        """
        
        results = self.db.execute_query(query)
        
        for row in results:
            print(f"  • {row['categoria']}: {row['activos']}/{row['total']} activos")
        
        # Mostrar prompt (primeras líneas)
        prompt_query = """
        SELECT valor FROM CONFIG_SISTEMA 
        WHERE categoria='PROMPT' AND clave='SISTEMA_BASE'
        """
        prompt_result = self.db.execute_query(prompt_query)
        
        if prompt_result:
            prompt = prompt_result[0]['valor']
            print(f"\n💬 PROMPT DEL SISTEMA (primeras 300 caracteres):")
            print("─" * 70)
            print(prompt[:300] + "...")
            print("─" * 70)


# Ejecutar población
if __name__ == "__main__":
    print("=" * 70)
    print("FASE 1 - POBLACIÓN DE CONFIG_SISTEMA")
    print("=" * 70)
    
    # Conectar a la base de datos
    db = DatabaseConnection()
    db.connect()
    
    # Poblar CONFIG_SISTEMA
    populator = ConfigSystemPopulator(db, 'database/schema/auto_discovery_results.json')
    total = populator.populate_all()
    
    # Mostrar resumen
    populator.show_summary()
    
    db.close()
    
    print("\n🎉 FASE 1 COMPLETADA - CONFIG_SISTEMA LISTA PARA USO")
