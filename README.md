# 🦷 IA Dental - Sistema Inteligente para Clínica Dental

Sistema de gestión dental con inteligencia artificial powered by **Google Gemini 2.5 Pro**.

## 🎯 Estado del Proyecto

**Progreso Global**: 45% completado

- ✅ **Fase 1** (80%): Scripts de conectividad y auto-descubrimiento creados
- ✅ **Fase 2** (100%): Gemini 2.5 Pro integrado y funcionando
- ⏳ **Fase 3** (0%): Auto-evaluación (pendiente)
- ⏳ **Fase 4** (0%): WhatsApp, RRSS (pendiente)

## 🏗️ Arquitectura

### Híbrida Local + Cloud

- **Local**: SQL Server (GELITE) - Datos sensibles de pacientes
- **Cloud**: Supabase - Configuraciones y comunicaciones
- **IA**: Google Gemini 2.5 Pro - Motor de inteligencia

### Componentes Principales

```
├── ai/                          # Módulos de IA
│   ├── gemini_client.py        # Cliente Gemini 2.5 Pro
│   ├── sql_generator.py        # Generador de SQL desde lenguaje natural
│   └── requirements.txt
├── scripts/phase1/              # Scripts de Fase 1
│   ├── db_connection.py        # Conexión a SQL Server
│   ├── db_proxy.py             # Proxy HTTP para server.js
│   ├── schema_extractor.py     # Extractor de esquema
│   ├── auto_discovery.py       # Auto-descubrimiento de reglas
│   ├── populate_config.py      # Poblador de CONFIG_SISTEMA
│   ├── generate_column_mappings.py  # Generador de mapeos
│   └── run_phase1.py           # Script maestro
├── database/schema/             # Esquemas y SQL
│   └── CONFIG_SISTEMA.sql      # Tabla de auto-configuración
└── docs/                        # Documentación
    ├── ARQUITECTURA_SISTEMA.md
    ├── ESTADO_PROYECTO.md
    └── CONFIGURAR_ACCESO_REMOTO.md
```

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.9+
- SQL Server 2008 R2+ (GELITE)
- Node.js 16+ (para server.js)
- API Key de Google Gemini

### Instalación

1. **Clonar repositorio:**
   ```bash
   git clone https://github.com/Manzanedodelgado/DENTAI.git
   cd DENTAI
   ```

2. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con tus credenciales
   ```

3. **Instalar dependencias Python:**
   ```bash
   cd scripts/phase1
   pip install -r requirements.txt
   ```

4. **Instalar dependencias Node.js:**
   ```bash
   npm install
   ```

### Ejecución

#### Opción 1: Desde Windows (Recomendado)

```cmd
cd scripts\phase1
python run_phase1.py
```

#### Opción 2: Usando Proxy HTTP

```bash
# En Windows: Iniciar server.js
node server.js

# En Mac/Linux: Ejecutar scripts
cd scripts/phase1
python3 run_phase1.py
```

## 🤖 Características de IA

### Gemini 2.5 Pro

- ✅ Generación de SQL desde lenguaje natural
- ✅ Validación de seguridad automática
- ✅ Conversiones de fechas/horas automáticas
- ✅ Mapeo de IDs a nombres legibles
- ✅ Auto-configuración dinámica

### Ejemplo de Uso

```python
from ai.gemini_client import GeminiAIClient
from ai.sql_generator import SQLGenerator

# Crear cliente
gemini = GeminiAIClient()
generator = SQLGenerator(gemini)

# Generar SQL desde lenguaje natural
result = generator.natural_language_query(
    "Muéstrame las citas de mañana con el Dr. Mario Rubio"
)

print(result['sql'])
# SELECT ... FROM DCitas WHERE ...
```

## 📊 Base de Datos

### Tabla Principal: DCitas (Citas)

| Columna BD | Nombre Coloquial | Tipo | Conversión |
|------------|------------------|------|------------|
| `Fecha` | Fecha Cita | INT | Días desde 1900-01-01 + 2 |
| `Hora` | Hora Cita | INT | Segundos desde medianoche |
| `Duracion` | Duración | INT | Segundos → minutos |
| `IdSitC` | Estado | INT | 0=Planificada, 7=Confirmada, etc. |

### CONFIG_SISTEMA

Tabla de auto-configuración que almacena:
- Prompts del sistema
- Reglas de negocio
- Descripciones de tablas
- Configuraciones dinámicas

## 🔒 Seguridad

- ✅ Credenciales en variables de entorno
- ✅ Validación de SQL (previene DROP, DELETE)
- ✅ Prepared statements
- ✅ Datos sensibles solo en local
- ✅ TrustServerCertificate para SQL Server

## 📝 Documentación

- [Arquitectura del Sistema](ARQUITECTURA_SISTEMA.md)
- [Estado del Proyecto](ESTADO_PROYECTO.md)
- [Configurar Acceso Remoto](CONFIGURAR_ACCESO_REMOTO.md)
- [Plan de Acción](PLAN_DE_ACCION.md)
- [Resumen Final](RESUMEN_FINAL.md)

## 🛠️ Desarrollo

### Estructura de Fases

1. **Fase 1**: Conectividad y Auto-Descubrimiento
2. **Fase 2**: Integración con Gemini 2.5 Pro
3. **Fase 3**: Auto-Evaluación y Auto-Corrección
4. **Fase 4**: WhatsApp, RRSS, Funcionalidades Avanzadas

### Próximos Pasos

- [ ] Ejecutar Fase 1 completa
- [ ] Implementar auto-evaluación
- [ ] Integrar WhatsApp Business
- [ ] Configurar Supabase
- [ ] Interfaz web de chat
- [ ] Módulo de voz (STT/TTS)

## 🤝 Contribuir

Este es un proyecto privado para la Clínica Dental Rubio García.

## 📄 Licencia

Propietario: Clínica Dental Rubio García

## 👥 Equipo

- **Desarrollo**: Juan Antonio Manzanedo
- **IA**: Google Gemini 2.5 Pro
- **Cliente**: Clínica Dental Rubio García

## 📞 Contacto

Para más información, contactar a través del repositorio.

---

**Powered by Google Gemini 2.5 Pro** 🤖
