#!/usr/bin/env python3
"""
Script de Configuración de Credenciales para Fase 1
Ayuda a configurar las credenciales de base de datos de forma segura
"""

import os
import sys
from pathlib import Path


def print_header(title):
    """Imprime un encabezado decorado"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def get_env_path():
    """Obtiene la ruta del archivo .env"""
    # Buscar .env en la raíz del proyecto (2 niveles arriba)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    env_path = project_root / '.env'
    return env_path


def read_current_env(env_path):
    """Lee el archivo .env actual"""
    env_vars = {}
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    
    return env_vars


def update_env_file(env_path, env_vars):
    """Actualiza el archivo .env con las nuevas variables"""
    
    # Leer contenido existente para preservar comentarios
    existing_lines = []
    if env_path.exists():
        with open(env_path, 'r') as f:
            existing_lines = f.readlines()
    
    # Actualizar o agregar variables
    updated_lines = []
    updated_keys = set()
    
    for line in existing_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and '=' in stripped:
            key = stripped.split('=', 1)[0]
            if key in env_vars:
                updated_lines.append(f"{key}={env_vars[key]}\n")
                updated_keys.add(key)
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)
    
    # Agregar nuevas variables que no existían
    for key, value in env_vars.items():
        if key not in updated_keys:
            updated_lines.append(f"{key}={value}\n")
    
    # Escribir archivo
    with open(env_path, 'w') as f:
        f.writelines(updated_lines)


def configure_database():
    """Configura las credenciales de base de datos"""
    
    print_header("🔐 CONFIGURACIÓN DE CREDENCIALES DE BASE DE DATOS")
    
    env_path = get_env_path()
    print(f"📁 Archivo .env: {env_path}")
    
    # Leer configuración actual
    current_env = read_current_env(env_path)
    
    print("\n📋 Configuración actual:")
    print(f"  DB_SERVER: {current_env.get('DB_SERVER', 'No configurado')}")
    print(f"  DB_INSTANCE: {current_env.get('DB_INSTANCE', 'No configurado')}")
    print(f"  DB_NAME: {current_env.get('DB_NAME', 'No configurado')}")
    print(f"  DB_USER: {'***' if current_env.get('DB_USER') else 'No configurado'}")
    print(f"  DB_PASSWORD: {'***' if current_env.get('DB_PASSWORD') else 'No configurado'}")
    
    print("\n" + "─" * 70)
    print("Ingresa las credenciales de la base de datos RUBIOGARCIADENTAL")
    print("(Presiona Enter para mantener el valor actual)")
    print("─" * 70 + "\n")
    
    # Solicitar credenciales
    db_server = input(f"DB_SERVER [{current_env.get('DB_SERVER', 'GABINETE2')}]: ").strip()
    if not db_server:
        db_server = current_env.get('DB_SERVER', 'GABINETE2')
    
    db_instance = input(f"DB_INSTANCE [{current_env.get('DB_INSTANCE', 'INFOMED')}]: ").strip()
    if not db_instance:
        db_instance = current_env.get('DB_INSTANCE', 'INFOMED')
    
    db_name = input(f"DB_NAME [{current_env.get('DB_NAME', 'GELITE')}]: ").strip()
    if not db_name:
        db_name = current_env.get('DB_NAME', 'GELITE')
    
    db_user = input(f"DB_USER [{current_env.get('DB_USER', '')}]: ").strip()
    if not db_user:
        db_user = current_env.get('DB_USER', '')
    
    # Importar getpass para ocultar la contraseña
    import getpass
    db_password = getpass.getpass(f"DB_PASSWORD [{'***' if current_env.get('DB_PASSWORD') else ''}]: ").strip()
    if not db_password:
        db_password = current_env.get('DB_PASSWORD', '')
    
    # Validar que todos los campos estén completos
    if not all([db_server, db_instance, db_name, db_user, db_password]):
        print("\n❌ ERROR: Todos los campos son obligatorios")
        return False
    
    # Actualizar .env
    new_env = current_env.copy()
    new_env.update({
        'DB_SERVER': db_server,
        'DB_INSTANCE': db_instance,
        'DB_NAME': db_name,
        'DB_USER': db_user,
        'DB_PASSWORD': db_password
    })
    
    update_env_file(env_path, new_env)
    
    print("\n✅ Credenciales guardadas en .env")
    
    # Probar conexión
    print("\n🔍 Probando conexión a base de datos...")
    
    try:
        # Importar módulo de conexión
        sys.path.insert(0, str(Path(__file__).parent))
        from db_connection import DatabaseConnection
        
        db = DatabaseConnection()
        db.connect()
        
        # Probar consulta simple
        result = db.execute_query("SELECT @@VERSION as version")
        print(f"✅ Conexión exitosa!")
        print(f"📡 SQL Server: {result[0]['version'][:80]}...")
        
        db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\nVerifica que:")
        print("  1. El servidor SQL Server esté accesible")
        print("  2. Las credenciales sean correctas")
        print("  3. El usuario tenga permisos en la base de datos")
        return False


def main():
    """Función principal"""
    
    success = configure_database()
    
    if success:
        print_header("🎉 CONFIGURACIÓN COMPLETADA")
        print("Ahora puedes ejecutar la Fase 1:")
        print("\n  cd scripts/phase1")
        print("  python3 run_phase1.py\n")
        return 0
    else:
        print_header("⚠️  CONFIGURACIÓN INCOMPLETA")
        print("Por favor, verifica las credenciales e intenta nuevamente.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
