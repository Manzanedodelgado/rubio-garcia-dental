"""
FASE 1 - Módulo de Conexión a Base de Datos
Gestión segura de conexión a SQL Server usando credenciales de RUBIOGARCIADENTAL
"""

import pyodbc
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class DatabaseConnection:
    """Gestiona la conexión segura a SQL Server"""
    
    def __init__(self):
        self.server = os.getenv('DB_SERVER', 'GABINETE2')
        self.instance = os.getenv('DB_INSTANCE', 'INFOMED')
        self.database = os.getenv('DB_NAME', 'GELITE')
        self.username = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.connection = None
        
        # Validar credenciales
        if not self.username or not self.password:
            raise ValueError("❌ ERROR: DB_USER y DB_PASSWORD deben estar configurados en .env")
    
    def connect(self):
        """Establece conexión a SQL Server"""
        try:
            # Construir connection string
            # Si instance está vacío, usar solo server (que puede incluir puerto)
            if self.instance:
                server_string = f'{self.server}\\{self.instance}'
            else:
                server_string = self.server
            
            conn_str = (
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={server_string};'
                f'DATABASE={self.database};'
                f'UID={self.username};'
                f'PWD={self.password};'
                f'TrustServerCertificate=yes;'
            )
            
            self.connection = pyodbc.connect(conn_str)
            print(f"✅ Conexión exitosa a {server_string} -> {self.database}")
            return self.connection
            
        except pyodbc.Error as e:
            print(f"❌ Error de conexión: {e}")
            raise
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL y retorna los resultados"""
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Si es SELECT, retornar resultados
            if query.strip().upper().startswith('SELECT'):
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
            else:
                # Para INSERT/UPDATE/DELETE
                self.connection.commit()
                return cursor.rowcount
                
        except pyodbc.Error as e:
            print(f"❌ Error ejecutando query: {e}")
            raise
        finally:
            cursor.close()
    
    def close(self):
        """Cierra la conexión"""
        if self.connection:
            self.connection.close()
            print("🔌 Conexión cerrada")


# Test de conexión
if __name__ == "__main__":
    print("🔍 Probando conexión a base de datos...")
    
    db = DatabaseConnection()
    db.connect()
    
    # Probar consulta simple
    result = db.execute_query("SELECT COUNT(*) as total FROM Pacientes")
    print(f"📊 Total de pacientes: {result[0]['total']}")
    
    db.close()
