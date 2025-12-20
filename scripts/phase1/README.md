# 🚀 FASE 1: Conectividad, Esquema e Ingeniería Inversa

## 📋 Descripción

Esta fase establece la base del sistema autónomo mediante:
- Conexión segura a la base de datos
- Extracción completa del esquema
- Auto-descubrimiento inteligente de reglas de negocio
- Creación y población de la tabla CONFIG_SISTEMA

## 🛠️ Instalación

### Requisitos Previos

1. **Python 3.8+**
2. **ODBC Driver 17 for SQL Server** (o superior)
3. **Acceso a la base de datos GELITE**

### Instalar Dependencias

```bash
cd scripts/phase1
pip install -r requirements.txt
```

### Configurar Variables de Entorno

Asegúrate de que tu archivo `.env` en la raíz del proyecto contenga:

```env
DB_SERVER=GABINETE2
DB_INSTANCE=INFOMED
DB_NAME=GELITE
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
```

## ▶️ Ejecución

### Opción 1: Script Maestro (Recomendado)

Ejecuta todo el proceso de Fase 1 automáticamente:

```bash
cd scripts/phase1
python run_phase1.py
```

Este script ejecutará en orden:
1. Conexión a base de datos
2. Extracción de esquema
3. Auto-descubrimiento de reglas
4. Creación de CONFIG_SISTEMA
5. Población de configuración inicial
6. Generación de DRF1

### Opción 2: Ejecución Manual por Pasos

Si prefieres ejecutar cada paso individualmente:

```bash
# 1. Probar conexión
python db_connection.py

# 2. Extraer esquema
python schema_extractor.py

# 3. Auto-descubrimiento
python auto_discovery.py

# 4. Poblar CONFIG_SISTEMA
python populate_config.py
```

## 📁 Archivos Generados

Después de ejecutar la Fase 1, se generarán:

- `database/schema/schema_extracted.json` - Esquema completo de la BD
- `database/schema/auto_discovery_results.json` - Reglas deducidas
- `database/schema/DRF1_Fase1_Resumen.md` - Documento resumen

## 🧪 Verificación

Para verificar que CONFIG_SISTEMA está correctamente poblada:

```sql
-- Ver resumen por categoría
SELECT categoria, COUNT(*) as total 
FROM CONFIG_SISTEMA 
GROUP BY categoria;

-- Ver el prompt del sistema
SELECT valor 
FROM CONFIG_SISTEMA 
WHERE categoria='PROMPT' AND clave='SISTEMA_BASE';

-- Ver reglas de negocio activas
SELECT clave, valor 
FROM CONFIG_SISTEMA 
WHERE categoria='REGLA_NEGOCIO' AND activo=1
ORDER BY prioridad;
```

## 🎯 Entregables (DRF1)

Al completar esta fase, obtendrás:

✅ Conexión verificada a base de datos  
✅ Esquema completo extraído (tablas, PK, FK, constraints)  
✅ Tabla CONFIG_SISTEMA creada y operativa  
✅ Reglas de negocio deducidas automáticamente  
✅ Prompt del sistema generado  
✅ Configuración inicial poblada  
✅ Documento DRF1 generado  

## 🐛 Solución de Problemas

### Error: "ODBC Driver not found"

Instala el driver ODBC:

**macOS:**
```bash
brew install msodbcsql17
```

**Linux:**
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17
```

**Windows:**
Descarga desde: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### Error: "Login failed for user"

Verifica que las credenciales en `.env` sean correctas y que el usuario tenga permisos de lectura/escritura en la base de datos GELITE.

### Error: "Table already exists"

Si CONFIG_SISTEMA ya existe, el script la eliminará y recreará. Si quieres preservar datos existentes, comenta la línea `DROP TABLE` en `CONFIG_SISTEMA.sql`.

## 📞 Soporte

Para problemas o preguntas sobre la Fase 1, consulta el plan de implementación principal o revisa los logs generados durante la ejecución.

---

**Siguiente Fase:** [FASE 2 - Motor de Lenguaje y Auto-Inyección](../phase2/README.md)
