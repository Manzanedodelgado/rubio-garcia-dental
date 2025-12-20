"""
ADAPTADOR: Usar server.js como proxy para acceso a BD
Mientras se configura el acceso remoto directo
"""

import requests
import json


class ServerJSProxy:
    """Usa el servidor Node.js existente como proxy para BD"""
    
    def __init__(self, base_url='http://192.168.1.34:3001'):
        self.base_url = base_url
        self.connection = None
    
    def execute_query(self, query, params=None):
        """Ejecuta query a través del servidor Node.js"""
        
        try:
            response = requests.post(
                f'{self.base_url}/api/query',
                json={'query': query},
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                rows = data.get('rows', [])
                
                # Convertir a formato compatible con pyodbc
                # pyodbc devuelve Row objects, pero podemos devolver dicts
                return rows
            else:
                error_data = response.json()
                raise Exception(f"Error del servidor: {error_data.get('error', 'Unknown error')}")
                
        except requests.exceptions.ConnectionError:
            raise Exception(f"❌ No se puede conectar al servidor Node.js en {self.base_url}")
        except requests.exceptions.Timeout:
            raise Exception("❌ Timeout al conectar con el servidor Node.js")
        except Exception as e:
            raise Exception(f"Error ejecutando query: {e}")
    
    def connect(self):
        """Verifica que el servidor esté disponible"""
        try:
            response = requests.get(f'{self.base_url}/api/health', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Conectado a servidor Node.js: {data.get('server')} -> {data.get('database')}")
                self.connection = True
                return True
            return False
        except requests.exceptions.ConnectionError:
            raise Exception(f"❌ Servidor Node.js no disponible en {self.base_url}")
        except Exception as e:
            raise Exception(f"❌ Error al conectar: {e}")
    
    def close(self):
        """No hace nada (HTTP es stateless)"""
        self.connection = None
        pass


# Test
if __name__ == "__main__":
    print("=" * 70)
    print("PRUEBA DE CONEXIÓN CON PROXY")
    print("=" * 70)
    
    print("\n⚠️  IMPORTANTE: Asegúrate de que el servidor Node.js esté corriendo:")
    print("   En Windows: cd C:\\IA-DENTAL\\rubio-garcia-dental-integrated && node server.js")
    print()
    
    try:
        proxy = ServerJSProxy()
        proxy.connect()
        
        # Probar consulta
        print("\n📝 Probando consulta...")
        result = proxy.execute_query("SELECT COUNT(*) as total FROM Pacientes")
        print(f"✅ Consulta exitosa: {result[0]['total']} pacientes")
        
        proxy.close()
        print("\n✅ Prueba completada exitosamente")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Solución:")
        print("   1. Abre CMD en Windows")
        print("   2. cd C:\\IA-DENTAL\\rubio-garcia-dental-integrated")
        print("   3. node server.js")
        print("   4. Vuelve a ejecutar este script")
