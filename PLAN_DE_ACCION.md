# 🎯 PLAN DE ACCIÓN - Configurar Acceso a Base de Datos

## 📊 Situación Actual

**Problema**: No se puede conectar a `GABINETE2\INFOMED` desde tu Mac
**Error**: `Login timeout expired`

---

## 🔧 OPCIÓN 2 SELECCIONADA: Configurar Acceso Remoto

### Documentos Creados:

1. **[CONFIGURAR_ACCESO_REMOTO.md](file:///Users/juanantoniomanzanedodelgado/Desktop/AGENTE%20IA/rubio-garcia-dental-integrated/CONFIGURAR_ACCESO_REMOTO.md)** 
   - Guía completa paso a paso
   - Configuración de SQL Server
   - Configuración de Firewall
   - Troubleshooting

2. **[db_proxy.py](file:///Users/juanantoniomanzanedodelgado/Desktop/AGENTE%20IA/rubio-garcia-dental-integrated/scripts/phase1/db_proxy.py)**
   - Adaptador para usar server.js como proxy
   - Solución temporal mientras configuras acceso remoto

---

## 📝 PASOS A SEGUIR

### PASO 1: En la Máquina Windows (GABINETE2)

Sigue la guía **CONFIGURAR_ACCESO_REMOTO.md**:

1. ✅ Habilitar TCP/IP en SQL Server Configuration Manager
2. ✅ Configurar puerto 1433
3. ✅ Reiniciar SQL Server
4. ✅ Habilitar autenticación SQL Server
5. ✅ Verificar usuario RUBIOGARCIADENTAL
6. ✅ Abrir puerto 1433 en Firewall de Windows
7. ✅ Obtener IP del servidor (ejecutar `ipconfig`)

### PASO 2: En tu Mac

1. Actualizar `.env` con la IP del servidor:
   ```env
   DB_SERVER=192.168.1.XXX  # IP de GABINETE2
   DB_INSTANCE=INFOMED
   DB_NAME=GELITE
   DB_USER=RUBIOGARCIADENTAL
   DB_PASSWORD=Y<666666
   ```

2. Probar conexión:
   ```bash
   cd scripts/phase1
   python3 -c "from db_connection import DatabaseConnection; db = DatabaseConnection(); db.connect()"
   ```

3. Si funciona, ejecutar Fase 1:
   ```bash
   python3 run_phase1.py
   ```

---

## 🔄 ALTERNATIVA: Usar server.js como Proxy (Temporal)

Si no puedes configurar acceso remoto inmediatamente:

### 1. Iniciar servidor Node.js

```bash
cd "/Users/juanantoniomanzanedodelgado/Desktop/AGENTE IA/rubio-garcia-dental-integrated"

# Si node no está en PATH, usar ruta completa:
/usr/local/bin/node server.js
# O
/opt/homebrew/bin/node server.js
```

### 2. Probar proxy

```bash
cd scripts/phase1
python3 db_proxy.py
```

### 3. Adaptar run_phase1.py para usar proxy

Modificar la línea 46 de `run_phase1.py`:

```python
# Cambiar:
from db_connection import DatabaseConnection
db = DatabaseConnection()

# Por:
from db_proxy import get_db_connection
db = get_db_connection()  # Intenta directo, si falla usa proxy
```

---

## ✅ Checklist de Configuración

### En Windows (GABINETE2):
- [ ] SQL Server Configuration Manager → TCP/IP habilitado
- [ ] Puerto 1433 configurado
- [ ] SQL Server reiniciado
- [ ] Autenticación SQL Server habilitada
- [ ] Usuario RUBIOGARCIADENTAL verificado
- [ ] Firewall → Puerto 1433 abierto
- [ ] IP del servidor obtenida (`ipconfig`)

### En Mac:
- [ ] .env actualizado con IP correcta
- [ ] Conexión probada
- [ ] Fase 1 ejecutada

---

## 🎯 Una Vez Configurado

Cuando la conexión funcione, ejecutar:

```bash
cd "/Users/juanantoniomanzanedodelgado/Desktop/AGENTE IA/rubio-garcia-dental-integrated/scripts/phase1"

# Ejecutar Fase 1 completa
python3 run_phase1.py

# Esto hará:
# 1. ✅ Conectar a GELITE
# 2. ✅ Extraer esquema completo
# 3. ✅ Crear CONFIG_SISTEMA
# 4. ✅ Auto-descubrir reglas
# 5. ✅ Generar mapeos desde CSV
# 6. ✅ Generar DRF1
```

---

## 📞 Comandos Útiles

### Verificar conectividad desde Mac:

```bash
# Ping al servidor
ping 192.168.1.XXX

# Verificar puerto 1433
nc -zv 192.168.1.XXX 1433
```

### Encontrar Node.js en Mac:

```bash
which node
# O
find /usr -name node 2>/dev/null
find /opt -name node 2>/dev/null
```

### Iniciar servidor Node.js:

```bash
# Opción 1: Si node está en PATH
node server.js

# Opción 2: Usar npm
npm start

# Opción 3: Ruta completa
/ruta/completa/a/node server.js
```

---

## 🚨 Si Nada Funciona

### Plan B: Ejecutar desde Windows

1. Copiar carpeta `scripts/phase1` a GABINETE2
2. Instalar Python en Windows
3. Instalar dependencias: `pip install pyodbc python-dotenv`
4. Ejecutar: `python run_phase1.py`

---

## 📊 Estado Actual del Proyecto

| Componente | Estado |
|------------|--------|
| Documentación | ✅ 100% |
| Scripts Fase 1 | ✅ Creados |
| Gemini 2.5 Pro | ✅ Funcionando |
| Conexión a BD | ❌ Pendiente configuración |
| Ejecución Fase 1 | ⏳ Bloqueado por conexión |

---

## 🎯 Próxima Acción

**AHORA**: Configurar acceso remoto siguiendo **CONFIGURAR_ACCESO_REMOTO.md**

**DESPUÉS**: Ejecutar `python3 run_phase1.py`

---

**¿Necesitas ayuda con algún paso específico de la configuración?**
