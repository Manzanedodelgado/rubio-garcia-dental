# 🔧 Guía: Configurar Acceso Remoto a SQL Server

## Objetivo
Permitir que tu Mac se conecte a `GABINETE2\INFOMED` (SQL Server) de forma remota.

---

## PASO 1: Configurar SQL Server (En la máquina Windows)

### 1.1 Habilitar TCP/IP

1. Abrir **SQL Server Configuration Manager**
2. Ir a: `SQL Server Network Configuration` → `Protocols for INFOMED`
3. Hacer clic derecho en **TCP/IP** → **Enable**
4. Hacer clic derecho en **TCP/IP** → **Properties**
5. En la pestaña **IP Addresses**:
   - Buscar **IPAll**
   - Configurar **TCP Port**: `1433`
6. **Reiniciar el servicio SQL Server**:
   - `SQL Server Services` → `SQL Server (INFOMED)` → Clic derecho → **Restart**

### 1.2 Habilitar Autenticación SQL Server

1. Abrir **SQL Server Management Studio (SSMS)**
2. Conectar al servidor
3. Clic derecho en el servidor → **Properties**
4. Ir a **Security**
5. Seleccionar: **SQL Server and Windows Authentication mode**
6. Clic en **OK**
7. **Reiniciar SQL Server**

### 1.3 Verificar/Crear Usuario RUBIOGARCIADENTAL

```sql
-- Verificar si existe
SELECT name FROM sys.sql_logins WHERE name = 'RUBIOGARCIADENTAL';

-- Si no existe, crear:
CREATE LOGIN RUBIOGARCIADENTAL WITH PASSWORD = 'Y<666666';

-- Dar permisos en GELITE
USE GELITE;
CREATE USER RUBIOGARCIADENTAL FOR LOGIN RUBIOGARCIADENTAL;
ALTER ROLE db_datareader ADD MEMBER RUBIOGARCIADENTAL;
ALTER ROLE db_datawriter ADD MEMBER RUBIOGARCIADENTAL;
ALTER ROLE db_ddladmin ADD MEMBER RUBIOGARCIADENTAL;
```

---

## PASO 2: Configurar Firewall de Windows

### 2.1 Abrir Puerto 1433

1. Abrir **Windows Defender Firewall**
2. Clic en **Advanced settings**
3. Clic en **Inbound Rules** → **New Rule**
4. Seleccionar **Port** → Next
5. Seleccionar **TCP** y escribir `1433` → Next
6. Seleccionar **Allow the connection** → Next
7. Marcar todas las opciones (Domain, Private, Public) → Next
8. Nombre: `SQL Server Port 1433` → Finish

### 2.2 Permitir SQL Server Browser (Opcional)

Si usas instancias nombradas:

1. **New Rule** → **Program**
2. Buscar: `C:\Program Files (x86)\Microsoft SQL Server\90\Shared\sqlbrowser.exe`
3. **Allow the connection**
4. Nombre: `SQL Server Browser`

---

## PASO 3: Obtener IP del Servidor

En la máquina Windows (GABINETE2):

```cmd
ipconfig
```

Buscar la **IPv4 Address** de tu red local (ejemplo: `192.168.1.100`)

---

## PASO 4: Actualizar .env en tu Mac

```env
# Cambiar de:
DB_SERVER=GABINETE2
DB_INSTANCE=INFOMED

# A (usando IP):
DB_SERVER=192.168.1.100
DB_INSTANCE=INFOMED

# O si no funciona con instancia:
DB_SERVER=192.168.1.100,1433
DB_INSTANCE=
```

---

## PASO 5: Probar Conexión desde tu Mac

```bash
cd "/Users/juanantoniomanzanedodelgado/Desktop/AGENTE IA/rubio-garcia-dental-integrated/scripts/phase1"

python3 -c "
from db_connection import DatabaseConnection
db = DatabaseConnection()
db.connect()
print('✅ Conexión exitosa!')
"
```

---

## PASO 6: Si Sigue Sin Funcionar

### Opción A: Verificar Conectividad de Red

```bash
# Desde tu Mac, hacer ping al servidor
ping 192.168.1.100

# Verificar que el puerto 1433 esté abierto
nc -zv 192.168.1.100 1433
```

### Opción B: Usar SQL Server Browser

Si usas instancia nombrada (`INFOMED`), necesitas SQL Server Browser:

1. En Windows: **Services** → **SQL Server Browser** → **Start**
2. Configurar para inicio automático

### Opción C: Deshabilitar Firewall Temporalmente (SOLO PARA PRUEBA)

```cmd
# En Windows (como Administrador)
netsh advfirewall set allprofiles state off

# Probar conexión desde Mac

# IMPORTANTE: Volver a habilitar
netsh advfirewall set allprofiles state on
```

---

## PASO 7: Configuración Alternativa (Sin Instancia)

Si la instancia nombrada causa problemas:

### En SQL Server Configuration Manager:

1. Ir a **SQL Server Services**
2. Verificar que el servicio sea `SQL Server (INFOMED)` o `MSSQLSERVER`
3. Si es `MSSQLSERVER` (instancia por defecto):

```env
# En .env:
DB_SERVER=192.168.1.100
DB_INSTANCE=
DB_NAME=GELITE
```

### Actualizar db_connection.py:

```python
# Si DB_INSTANCE está vacío, no usar instancia
if self.instance:
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server}\\{self.instance};...'
else:
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};...'
```

---

## PASO 8: Ejecutar Fase 1

Una vez que la conexión funcione:

```bash
cd scripts/phase1
python3 run_phase1.py
```

---

## 🔍 Troubleshooting

### Error: "Login failed for user"
- Verificar usuario y contraseña
- Verificar que el usuario tenga permisos en GELITE

### Error: "Cannot connect to server"
- Verificar firewall
- Verificar que SQL Server esté corriendo
- Verificar IP del servidor

### Error: "Named Pipes Provider"
- Habilitar TCP/IP en SQL Server Configuration Manager
- Reiniciar SQL Server

### Error: "Timeout expired"
- Verificar conectividad de red
- Aumentar timeout en db_connection.py:
  ```python
  conn_str += 'Connection Timeout=30;'
  ```

---

## 📞 Comandos Útiles

```bash
# Verificar ODBC Driver instalado
odbcinst -q -d

# Probar conexión con sqlcmd (si está instalado)
sqlcmd -S 192.168.1.100,1433 -U RUBIOGARCIADENTAL -P 'Y<666666' -d GELITE

# Ver logs de SQL Server (Windows)
# C:\Program Files\Microsoft SQL Server\MSSQL15.INFOMED\MSSQL\Log\ERRORLOG
```

---

## ✅ Checklist de Configuración

- [ ] TCP/IP habilitado en SQL Server
- [ ] Puerto 1433 configurado
- [ ] SQL Server reiniciado
- [ ] Autenticación SQL Server habilitada
- [ ] Usuario RUBIOGARCIADENTAL creado con permisos
- [ ] Firewall configurado (puerto 1433 abierto)
- [ ] IP del servidor obtenida
- [ ] .env actualizado con IP correcta
- [ ] Conexión probada desde Mac
- [ ] Fase 1 ejecutada exitosamente

---

**Siguiente paso**: Una vez configurado, ejecutar `python3 run_phase1.py`
