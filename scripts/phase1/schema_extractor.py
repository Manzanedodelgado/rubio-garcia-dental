"""
FASE 1 - Extractor de Esquema de Base de Datos
Extrae metadatos completos: tablas, columnas, PK, FK, constraints, tipos de datos
"""

import json
from datetime import datetime
from db_connection import DatabaseConnection


class SchemaExtractor:
    """Extrae el esquema completo de la base de datos"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.schema = {
            'metadata': {
                'extracted_at': datetime.now().isoformat(),
                'database': db_connection.database,
                'server': db_connection.server
            },
            'tables': []
        }
    
    def extract_tables(self):
        """Extrae lista de tablas del esquema"""
        query = """
        SELECT 
            TABLE_NAME,
            TABLE_TYPE
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
        """
        
        tables = self.db.execute_query(query)
        print(f"📋 Encontradas {len(tables)} tablas")
        return tables
    
    def extract_columns(self, table_name):
        """Extrae columnas de una tabla específica"""
        query = """
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            IS_NULLABLE,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = ?
        ORDER BY ORDINAL_POSITION
        """
        
        columns = self.db.execute_query(query, [table_name])
        return columns
    
    def extract_primary_keys(self, table_name):
        """Extrae primary keys de una tabla"""
        query = """
        SELECT 
            COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + CONSTRAINT_NAME), 'IsPrimaryKey') = 1
        AND TABLE_NAME = ?
        """
        
        pks = self.db.execute_query(query, [table_name])
        return [pk['COLUMN_NAME'] for pk in pks]
    
    def extract_foreign_keys(self, table_name):
        """Extrae foreign keys de una tabla"""
        query = """
        SELECT 
            fk.name AS FK_NAME,
            OBJECT_NAME(fk.parent_object_id) AS TABLE_NAME,
            COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS COLUMN_NAME,
            OBJECT_NAME(fk.referenced_object_id) AS REFERENCED_TABLE,
            COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS REFERENCED_COLUMN
        FROM sys.foreign_keys AS fk
        INNER JOIN sys.foreign_key_columns AS fkc 
            ON fk.object_id = fkc.constraint_object_id
        WHERE OBJECT_NAME(fk.parent_object_id) = ?
        """
        
        fks = self.db.execute_query(query, [table_name])
        return fks
    
    def extract_check_constraints(self, table_name):
        """Extrae CHECK constraints de una tabla"""
        query = """
        SELECT 
            cc.name AS CONSTRAINT_NAME,
            cc.definition AS CHECK_CLAUSE
        FROM sys.check_constraints cc
        WHERE OBJECT_NAME(cc.parent_object_id) = ?
        """
        
        checks = self.db.execute_query(query, [table_name])
        return checks
    
    def extract_unique_constraints(self, table_name):
        """Extrae UNIQUE constraints"""
        query = """
        SELECT 
            COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + CONSTRAINT_NAME), 'IsUniqueCnst') = 1
        AND TABLE_NAME = ?
        """
        
        uniques = self.db.execute_query(query, [table_name])
        return [u['COLUMN_NAME'] for u in uniques]
    
    def extract_full_schema(self):
        """Extrae el esquema completo de todas las tablas"""
        print("🔍 Iniciando extracción de esquema completo...")
        
        tables = self.extract_tables()
        
        for table in tables:
            table_name = table['TABLE_NAME']
            print(f"  📊 Procesando tabla: {table_name}")
            
            table_info = {
                'name': table_name,
                'columns': self.extract_columns(table_name),
                'primary_keys': self.extract_primary_keys(table_name),
                'foreign_keys': self.extract_foreign_keys(table_name),
                'check_constraints': self.extract_check_constraints(table_name),
                'unique_constraints': self.extract_unique_constraints(table_name)
            }
            
            self.schema['tables'].append(table_info)
        
        print(f"✅ Esquema completo extraído: {len(self.schema['tables'])} tablas")
        return self.schema
    
    def save_to_file(self, filename='schema_output.json'):
        """Guarda el esquema en un archivo JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.schema, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Esquema guardado en: {filename}")
        return filename


# Ejecutar extracción
if __name__ == "__main__":
    print("=" * 60)
    print("FASE 1 - EXTRACCIÓN DE ESQUEMA DE BASE DE DATOS")
    print("=" * 60)
    
    # Conectar a la base de datos
    db = DatabaseConnection()
    db.connect()
    
    # Extraer esquema
    extractor = SchemaExtractor(db)
    schema = extractor.extract_full_schema()
    
    # Guardar en archivo
    output_file = 'database/schema/schema_extracted.json'
    extractor.save_to_file(output_file)
    
    # Mostrar resumen
    print("\n📈 RESUMEN:")
    print(f"  - Total de tablas: {len(schema['tables'])}")
    print(f"  - Archivo generado: {output_file}")
    
    # Mostrar algunas tablas principales
    print("\n📋 Tablas principales encontradas:")
    for table in schema['tables'][:10]:
        pk_count = len(table['primary_keys'])
        fk_count = len(table['foreign_keys'])
        col_count = len(table['columns'])
        print(f"  • {table['name']}: {col_count} columnas, {pk_count} PK, {fk_count} FK")
    
    db.close()
