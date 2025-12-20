"""
FASE 1 - Algoritmo de Auto-Descubrimiento Inteligente
Analiza el esquema y deduce automáticamente:
- Prompt del sistema inicial
- Reglas de negocio
- Validaciones
- Descripciones de tablas
"""

import json
import re
from datetime import datetime
from db_connection import DatabaseConnection


class AutoDiscoveryEngine:
    """Motor de auto-descubrimiento que analiza el esquema y deduce configuración"""
    
    def __init__(self, schema_file='database/schema/schema_extracted.json'):
        with open(schema_file, 'r', encoding='utf-8') as f:
            self.schema = json.load(f)
        
        self.discovered_rules = []
        self.table_descriptions = {}
        self.system_prompt = ""
    
    def analyze_column_semantics(self, column_name, data_type):
        """Analiza el nombre de la columna y deduce su propósito"""
        column_lower = column_name.lower()
        rules = []
        
        # Reglas contables
        if any(keyword in column_lower for keyword in ['saldo', 'importe', 'precio', 'total', 'coste', 'cost']):
            rules.append({
                'type': 'VALIDACION_CONTABLE',
                'column': column_name,
                'rule': 'debe_ser_numerico_positivo',
                'message': f'{column_name} debe ser un valor numérico positivo o cero'
            })
        
        # Validaciones de fecha
        if any(keyword in column_lower for keyword in ['fecha', 'fec', 'date']):
            rules.append({
                'type': 'VALIDACION_TEMPORAL',
                'column': column_name,
                'rule': 'formato_fecha_valido',
                'message': f'{column_name} debe tener un formato de fecha válido'
            })
        
        # Validaciones de email
        if 'email' in column_lower or 'correo' in column_lower:
            rules.append({
                'type': 'VALIDACION_FORMATO',
                'column': column_name,
                'rule': 'formato_email',
                'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                'message': f'{column_name} debe tener formato de email válido'
            })
        
        # Validaciones de teléfono
        if any(keyword in column_lower for keyword in ['tel', 'telefono', 'phone', 'movil']):
            rules.append({
                'type': 'VALIDACION_FORMATO',
                'column': column_name,
                'rule': 'formato_telefono',
                'pattern': r'^\+?[0-9]{9,15}$',
                'message': f'{column_name} debe tener formato de teléfono válido'
            })
        
        # Estados y status
        if any(keyword in column_lower for keyword in ['estado', 'status', 'situacion', 'sit']):
            rules.append({
                'type': 'MAQUINA_ESTADOS',
                'column': column_name,
                'rule': 'validar_transicion_estado',
                'message': f'{column_name} debe tener un valor de estado válido'
            })
        
        # Campos de identificación
        if any(keyword in column_lower for keyword in ['nif', 'dni', 'cif']):
            rules.append({
                'type': 'VALIDACION_FORMATO',
                'column': column_name,
                'rule': 'formato_nif',
                'message': f'{column_name} debe tener formato de NIF/DNI válido'
            })
        
        return rules
    
    def deduce_table_purpose(self, table_name, columns, foreign_keys):
        """Deduce el propósito de una tabla basándose en su nombre y estructura"""
        table_lower = table_name.lower()
        
        # Tablas de pacientes
        if 'paciente' in table_lower or 'patient' in table_lower:
            return "Almacena información de pacientes de la clínica dental"
        
        # Tablas de citas
        if 'cita' in table_lower or 'appointment' in table_lower:
            return "Gestiona las citas y agendamiento de pacientes"
        
        # Tablas de tratamientos
        if 'tratamiento' in table_lower or 'treatment' in table_lower or 'tto' in table_lower:
            return "Registra los tratamientos dentales realizados"
        
        # Tablas de presupuestos
        if 'presup' in table_lower or 'budget' in table_lower:
            return "Gestiona presupuestos y estimaciones de tratamientos"
        
        # Tablas de facturación
        if 'factura' in table_lower or 'invoice' in table_lower:
            return "Maneja la facturación y cobros"
        
        # Tablas de colaboradores/doctores
        if 'colabo' in table_lower or 'doctor' in table_lower or 'medico' in table_lower:
            return "Información de doctores y colaboradores de la clínica"
        
        # Tablas de configuración (tipo catálogo)
        if table_name.startswith('T') and len(foreign_keys) == 0:
            return f"Tabla de catálogo/configuración para {table_name}"
        
        # Tablas intermedias (muchos a muchos)
        if len(foreign_keys) >= 2:
            return f"Tabla de relación entre {foreign_keys[0]['REFERENCED_TABLE']} y {foreign_keys[1]['REFERENCED_TABLE']}"
        
        return f"Tabla de datos: {table_name}"
    
    def analyze_relationships(self, table):
        """Analiza las relaciones de una tabla"""
        rules = []
        
        for fk in table['foreign_keys']:
            rules.append({
                'type': 'INTEGRIDAD_REFERENCIAL',
                'table': table['name'],
                'column': fk['COLUMN_NAME'],
                'references': fk['REFERENCED_TABLE'],
                'referenced_column': fk['REFERENCED_COLUMN'],
                'rule': 'validar_existencia_registro',
                'message': f"El valor de {fk['COLUMN_NAME']} debe existir en {fk['REFERENCED_TABLE']}.{fk['REFERENCED_COLUMN']}"
            })
        
        return rules
    
    def analyze_constraints(self, table):
        """Analiza los constraints de una tabla"""
        rules = []
        
        # NOT NULL constraints
        for column in table['columns']:
            if column['IS_NULLABLE'] == 'NO':
                rules.append({
                    'type': 'CAMPO_OBLIGATORIO',
                    'table': table['name'],
                    'column': column['COLUMN_NAME'],
                    'rule': 'no_nulo',
                    'message': f"{column['COLUMN_NAME']} es un campo obligatorio"
                })
        
        # UNIQUE constraints
        for unique_col in table['unique_constraints']:
            rules.append({
                'type': 'UNICIDAD',
                'table': table['name'],
                'column': unique_col,
                'rule': 'valor_unico',
                'message': f"{unique_col} debe ser único en la tabla {table['name']}"
            })
        
        # CHECK constraints
        for check in table['check_constraints']:
            rules.append({
                'type': 'VALIDACION_CHECK',
                'table': table['name'],
                'constraint_name': check['CONSTRAINT_NAME'],
                'definition': check['CHECK_CLAUSE'],
                'rule': 'validar_condicion',
                'message': f"Debe cumplir: {check['CHECK_CLAUSE']}"
            })
        
        return rules
    
    def discover_all_rules(self):
        """Ejecuta el proceso completo de auto-descubrimiento"""
        print("🔍 Iniciando Auto-Descubrimiento Inteligente...")
        
        all_rules = []
        
        for table in self.schema['tables']:
            table_name = table['name']
            print(f"  🔎 Analizando: {table_name}")
            
            # Deducir propósito de la tabla
            purpose = self.deduce_table_purpose(
                table_name, 
                table['columns'], 
                table['foreign_keys']
            )
            self.table_descriptions[table_name] = purpose
            
            # Analizar semántica de columnas
            for column in table['columns']:
                column_rules = self.analyze_column_semantics(
                    column['COLUMN_NAME'],
                    column['DATA_TYPE']
                )
                for rule in column_rules:
                    rule['table'] = table_name
                    all_rules.append(rule)
            
            # Analizar relaciones
            relationship_rules = self.analyze_relationships(table)
            all_rules.extend(relationship_rules)
            
            # Analizar constraints
            constraint_rules = self.analyze_constraints(table)
            all_rules.extend(constraint_rules)
        
        self.discovered_rules = all_rules
        print(f"✅ Auto-Descubrimiento completado: {len(all_rules)} reglas deducidas")
        
        return all_rules
    
    def generate_system_prompt(self):
        """Genera el prompt inicial del sistema basado en el análisis"""
        
        # Contar tablas principales
        main_tables = [t for t in self.schema['tables'] if not t['name'].startswith('T')]
        catalog_tables = [t for t in self.schema['tables'] if t['name'].startswith('T')]
        
        prompt = f"""Eres Alveolo, un asistente de inteligencia artificial especializado en la gestión de la clínica dental Rubio García.

**TU MISIÓN:**
Ayudar al personal de la clínica a consultar y gestionar información de pacientes, citas, tratamientos y presupuestos de manera eficiente y segura.

**BASE DE DATOS:**
Tienes acceso a una base de datos SQL Server llamada GELITE con {len(self.schema['tables'])} tablas:
- {len(main_tables)} tablas principales de datos
- {len(catalog_tables)} tablas de catálogo/configuración

**TABLAS PRINCIPALES:**
"""
        
        # Listar tablas principales con sus descripciones
        for table_name, description in sorted(self.table_descriptions.items())[:15]:
            if not table_name.startswith('T'):
                prompt += f"• {table_name}: {description}\n"
        
        prompt += f"""
**CAPACIDADES:**
1. Consultar información de pacientes, citas, tratamientos y presupuestos
2. Generar consultas SQL optimizadas basadas en lenguaje natural
3. Validar datos antes de realizar operaciones de escritura
4. Proporcionar estadísticas y análisis de la clínica
5. Responder preguntas sobre el estado de pacientes y agenda

**REGLAS DE NEGOCIO DETECTADAS AUTOMÁTICAMENTE:**
{len(self.discovered_rules)} reglas de validación y negocio han sido identificadas en el esquema.

**INSTRUCCIONES:**
- Siempre valida los datos contra las reglas de negocio antes de escribir
- Usa prepared statements para prevenir inyección SQL
- Proporciona respuestas claras y profesionales en español
- Si no estás seguro de algo, pregunta antes de actuar
- Registra todas las operaciones importantes en el historial

**IDIOMA:** Español (España)
**TONO:** Profesional, amable y eficiente
"""
        
        self.system_prompt = prompt
        return prompt
    
    def save_discoveries(self, output_file='database/schema/auto_discovery_results.json'):
        """Guarda los resultados del auto-descubrimiento"""
        
        results = {
            'metadata': {
                'discovered_at': datetime.now().isoformat(),
                'total_rules': len(self.discovered_rules),
                'total_tables_analyzed': len(self.schema['tables'])
            },
            'system_prompt': self.system_prompt,
            'table_descriptions': self.table_descriptions,
            'business_rules': self.discovered_rules
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Resultados guardados en: {output_file}")
        return output_file


# Ejecutar auto-descubrimiento
if __name__ == "__main__":
    print("=" * 70)
    print("FASE 1 - AUTO-DESCUBRIMIENTO INTELIGENTE")
    print("=" * 70)
    
    # Cargar esquema extraído
    engine = AutoDiscoveryEngine('database/schema/schema_extracted.json')
    
    # Descubrir reglas
    rules = engine.discover_all_rules()
    
    # Generar prompt del sistema
    prompt = engine.generate_system_prompt()
    
    # Guardar resultados
    output_file = 'database/schema/auto_discovery_results.json'
    engine.save_discoveries(output_file)
    
    # Mostrar resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE AUTO-DESCUBRIMIENTO:")
    print("=" * 70)
    print(f"✅ Total de reglas deducidas: {len(rules)}")
    print(f"✅ Tablas analizadas: {len(engine.table_descriptions)}")
    print(f"✅ Prompt del sistema generado: {len(prompt)} caracteres")
    
    # Mostrar distribución de reglas por tipo
    rule_types = {}
    for rule in rules:
        rule_type = rule['type']
        rule_types[rule_type] = rule_types.get(rule_type, 0) + 1
    
    print("\n📈 Distribución de reglas por tipo:")
    for rule_type, count in sorted(rule_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {rule_type}: {count} reglas")
    
    print("\n💡 Ejemplos de reglas deducidas:")
    for i, rule in enumerate(rules[:5], 1):
        print(f"  {i}. [{rule['type']}] {rule.get('table', 'N/A')}.{rule.get('column', 'N/A')}")
        print(f"     → {rule['message']}")
    
    print(f"\n📄 Archivo completo: {output_file}")
