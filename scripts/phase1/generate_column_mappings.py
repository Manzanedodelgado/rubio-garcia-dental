"""
Script para procesar el archivo CSV de columnas y crear mapeos automáticos
Lee NOMBRE DE COLUMNAS.csv y genera:
1. Tabla MAPEO_COLUMNAS poblada
2. Documentación de estructura de BD para Gemini
"""

import csv
from collections import defaultdict
from db_connection import DatabaseConnection


class ColumnMappingGenerator:
    """Genera mapeos de columnas desde el CSV"""
    
    def __init__(self, csv_file, db_connection):
        self.csv_file = csv_file
        self.db = db_connection
        self.tables = defaultdict(list)
        
    def parse_csv(self):
        """Lee el CSV y organiza por tablas"""
        print(f"📖 Leyendo {self.csv_file}...")
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            # El CSV tiene formato: Tabla;Columna
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split(';')
                if len(parts) == 2:
                    table_name, column_name = parts
                    self.tables[table_name].append(column_name)
        
        print(f"✅ Encontradas {len(self.tables)} tablas")
        return self.tables
    
    def create_mapeo_columnas_table(self):
        """Crea la tabla MAPEO_COLUMNAS"""
        print("📋 Creando tabla MAPEO_COLUMNAS...")
        
        sql = """
        IF OBJECT_ID('MAPEO_COLUMNAS', 'U') IS NOT NULL
            DROP TABLE MAPEO_COLUMNAS;
        
        CREATE TABLE MAPEO_COLUMNAS (
            id INT IDENTITY(1,1) PRIMARY KEY,
            tabla VARCHAR(100) NOT NULL,
            columna_bd VARCHAR(100) NOT NULL,
            nombre_coloquial VARCHAR(100),
            tipo_dato VARCHAR(50),
            es_fecha BIT DEFAULT 0,
            es_hora BIT DEFAULT 0,
            es_duracion BIT DEFAULT 0,
            es_estado BIT DEFAULT 0,
            formula_conversion NVARCHAR(MAX),
            descripcion NVARCHAR(500),
            UNIQUE(tabla, columna_bd)
        );
        
        CREATE INDEX idx_mapeo_tabla ON MAPEO_COLUMNAS(tabla);
        """
        
        try:
            self.db.execute_query(sql)
            print("✅ Tabla MAPEO_COLUMNAS creada")
        except Exception as e:
            print(f"⚠️  {e}")
    
    def deduce_column_type(self, table_name, column_name):
        """Deduce el tipo y propósito de una columna"""
        col_lower = column_name.lower()
        
        # Fechas
        if any(x in col_lower for x in ['fecha', 'fec', 'date']):
            if table_name == 'DCitas' and column_name == 'Fecha':
                return {
                    'tipo': 'FECHA_DIAS',
                    'es_fecha': 1,
                    'formula': "CONVERT(VARCHAR(10), DATEADD(DAY, Fecha - 2, '1900-01-01'), 23)",
                    'descripcion': 'Fecha almacenada como días desde 1900-01-01'
                }
            return {
                'tipo': 'FECHA',
                'es_fecha': 1,
                'formula': None,
                'descripcion': 'Campo de fecha'
            }
        
        # Horas
        if any(x in col_lower for x in ['hora', 'hor', 'time']):
            if table_name == 'DCitas' and column_name == 'Hora':
                return {
                    'tipo': 'HORA_SEGUNDOS',
                    'es_hora': 1,
                    'formula': "CONVERT(VARCHAR(5), DATEADD(SECOND, Hora, 0), 108)",
                    'descripcion': 'Hora almacenada como segundos desde medianoche'
                }
            return {
                'tipo': 'HORA',
                'es_hora': 1,
                'formula': None,
                'descripcion': 'Campo de hora'
            }
        
        # Duración
        if 'duracion' in col_lower or 'duration' in col_lower:
            return {
                'tipo': 'DURACION_MINUTOS',
                'es_duracion': 1,
                'formula': "CAST(CAST(Duracion AS DECIMAL(10, 2)) / 60 AS INT)",
                'descripcion': 'Duración en segundos, convertida a minutos'
            }
        
        # Estados
        if any(x in col_lower for x in ['estado', 'status', 'sitc', 'sit']):
            return {
                'tipo': 'ESTADO',
                'es_estado': 1,
                'formula': None,
                'descripcion': 'Campo de estado (requiere mapeo de valores)'
            }
        
        # IDs
        if col_lower.startswith('id'):
            return {
                'tipo': 'ID',
                'es_fecha': 0,
                'formula': None,
                'descripcion': f'Identificador: {column_name}'
            }
        
        # Default
        return {
            'tipo': 'TEXTO',
            'es_fecha': 0,
            'formula': None,
            'descripcion': None
        }
    
    def populate_mappings(self, priority_tables=None):
        """Popula la tabla MAPEO_COLUMNAS"""
        if priority_tables is None:
            priority_tables = ['DCitas', 'Pacientes', 'Tratamientos', 'Presu', 'TtosMed']
        
        print(f"📝 Poblando mapeos para tablas prioritarias: {', '.join(priority_tables)}")
        
        insert_sql = """
        INSERT INTO MAPEO_COLUMNAS 
        (tabla, columna_bd, nombre_coloquial, tipo_dato, es_fecha, es_hora, es_duracion, es_estado, formula_conversion, descripcion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        total_inserted = 0
        
        for table_name in priority_tables:
            if table_name not in self.tables:
                print(f"⚠️  Tabla {table_name} no encontrada en CSV")
                continue
            
            columns = self.tables[table_name]
            print(f"  📊 {table_name}: {len(columns)} columnas")
            
            for column_name in columns:
                # Deducir tipo
                col_info = self.deduce_column_type(table_name, column_name)
                
                # Nombre coloquial (por ahora igual al nombre de columna)
                nombre_coloquial = column_name
                
                try:
                    self.db.execute_query(insert_sql, [
                        table_name,
                        column_name,
                        nombre_coloquial,
                        col_info['tipo'],
                        col_info.get('es_fecha', 0),
                        col_info.get('es_hora', 0),
                        col_info.get('es_duracion', 0),
                        col_info.get('es_estado', 0),
                        col_info.get('formula'),
                        col_info.get('descripcion')
                    ])
                    total_inserted += 1
                except Exception as e:
                    print(f"⚠️  Error insertando {table_name}.{column_name}: {e}")
        
        print(f"✅ {total_inserted} mapeos insertados")
        return total_inserted
    
    def generate_documentation(self, output_file='database/schema/estructura_bd.md'):
        """Genera documentación de la estructura de BD"""
        print(f"📄 Generando documentación en {output_file}...")
        
        content = f"""# Estructura de Base de Datos GELITE

**Generado automáticamente desde NOMBRE DE COLUMNAS.csv**

Total de tablas: {len(self.tables)}

## Tablas Principales

"""
        
        # Tablas prioritarias con descripción
        priority_info = {
            'DCitas': 'Gestión de citas y agendamiento',
            'Pacientes': 'Información de pacientes',
            'Tratamientos': 'Catálogo de tratamientos',
            'TtosMed': 'Tratamientos médicos realizados',
            'Presu': 'Presupuestos',
            'TColabos': 'Colaboradores/Odontólogos',
            'Clientes': 'Clientes/Aseguradoras',
        }
        
        for table_name, description in priority_info.items():
            if table_name in self.tables:
                columns = self.tables[table_name]
                content += f"### {table_name}\n"
                content += f"**Descripción**: {description}\n"
                content += f"**Columnas**: {len(columns)}\n\n"
                
                # Listar columnas importantes
                important_cols = [c for c in columns if any(x in c.lower() for x in ['id', 'nombre', 'fecha', 'estado'])]
                if important_cols:
                    content += "**Columnas clave**:\n"
                    for col in important_cols[:10]:
                        content += f"- `{col}`\n"
                    content += "\n"
        
        content += f"""
## Todas las Tablas

Total: {len(self.tables)} tablas

"""
        
        for table_name in sorted(self.tables.keys()):
            content += f"- **{table_name}** ({len(self.tables[table_name])} columnas)\n"
        
        # Guardar
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Documentación generada: {output_file}")


def main():
    """Ejecuta el proceso completo"""
    print("=" * 70)
    print("GENERADOR DE MAPEOS DE COLUMNAS")
    print("=" * 70)
    
    # Conectar a BD
    db = DatabaseConnection()
    db.connect()
    
    # Crear generador
    csv_file = '../../NOMBRE DE COLUMNAS.csv'
    generator = ColumnMappingGenerator(csv_file, db)
    
    # Parsear CSV
    tables = generator.parse_csv()
    
    # Crear tabla
    generator.create_mapeo_columnas_table()
    
    # Poblar mapeos
    total = generator.populate_mappings()
    
    # Generar documentación
    generator.generate_documentation()
    
    # Resumen
    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)
    print(f"📊 Tablas procesadas: {len(tables)}")
    print(f"📝 Mapeos creados: {total}")
    print(f"📄 Documentación: database/schema/estructura_bd.md")
    
    db.close()


if __name__ == "__main__":
    main()
