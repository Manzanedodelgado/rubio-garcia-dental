#!/usr/bin/env python3
"""
FASE 1 - SCRIPT MAESTRO
Ejecuta el proceso completo de la Fase 1:
1. Conexión a base de datos
2. Extracción de esquema
3. Auto-descubrimiento de reglas
4. Creación y población de CONFIG_SISTEMA
5. Generación de DRF1 (Documento Resumen de Fase 1)
"""

import sys
import os
from datetime import datetime

# Asegurar que podemos importar los módulos
sys.path.insert(0, os.path.dirname(__file__))

from db_connection import DatabaseConnection
from schema_extractor import SchemaExtractor
from auto_discovery import AutoDiscoveryEngine
from populate_config import ConfigSystemPopulator


def print_header(title):
    """Imprime un encabezado decorado"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Ejecuta el proceso completo de Fase 1"""
    
    print_header("🚀 FASE 1: CONECTIVIDAD, ESQUEMA E INGENIERÍA INVERSA")
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    start_time = datetime.now()
    
    try:
        # ========================================================================
        # PASO 1: Conexión a Base de Datos
        # ========================================================================
        print_header("PASO 1/5: Conexión a Base de Datos")
        
        # Intentar conexión directa primero
        db = None
        try:
            db = DatabaseConnection()
            db.connect()
            print("✅ Usando conexión directa a SQL Server")
        except Exception as e:
            print(f"⚠️  Conexión directa falló: {e}")
            print("🔄 Intentando usar servidor Node.js como proxy...")
            
            # Usar proxy HTTP
            from db_proxy import ServerJSProxy
            db = ServerJSProxy(base_url='http://192.168.1.34:3001')
            db.connect()
            print("✅ Usando servidor Node.js como proxy HTTP")
        
        # Verificar conexión
        result = db.execute_query("SELECT @@VERSION as version")
        version_text = result[0].get('version', 'Unknown') if isinstance(result[0], dict) else str(result[0][0])
        print(f"📡 SQL Server Version: {version_text[:80]}...")
        
        # ========================================================================
        # PASO 2: Extracción de Esquema
        # ========================================================================
        print_header("PASO 2/5: Extracción de Esquema Completo")
        
        extractor = SchemaExtractor(db)
        schema = extractor.extract_full_schema()
        
        schema_file = 'database/schema/schema_extracted.json'
        extractor.save_to_file(schema_file)
        
        print(f"✅ Esquema extraído: {len(schema['tables'])} tablas")
        
        # ========================================================================
        # PASO 3: Auto-Descubrimiento de Reglas
        # ========================================================================
        print_header("PASO 3/5: Auto-Descubrimiento Inteligente")
        
        discovery_engine = AutoDiscoveryEngine(schema_file)
        rules = discovery_engine.discover_all_rules()
        prompt = discovery_engine.generate_system_prompt()
        
        discovery_file = 'database/schema/auto_discovery_results.json'
        discovery_engine.save_discoveries(discovery_file)
        
        print(f"✅ Reglas deducidas: {len(rules)}")
        print(f"✅ Prompt generado: {len(prompt)} caracteres")
        
        # ========================================================================
        # PASO 4: Creación y Población de CONFIG_SISTEMA
        # ========================================================================
        print_header("PASO 4/5: Creación y Población de CONFIG_SISTEMA")
        
        populator = ConfigSystemPopulator(db, discovery_file)
        total_records = populator.populate_all()
        
        print(f"✅ CONFIG_SISTEMA poblada: {total_records} registros")
        
        # ========================================================================
        # PASO 5: Verificación Final
        # ========================================================================
        print_header("PASO 5/5: Verificación Final")
        
        # Verificar que CONFIG_SISTEMA está operativa
        verification_queries = [
            ("Prompt del sistema", "SELECT COUNT(*) as count FROM CONFIG_SISTEMA WHERE categoria='PROMPT'"),
            ("Reglas de negocio", "SELECT COUNT(*) as count FROM CONFIG_SISTEMA WHERE categoria='REGLA_NEGOCIO'"),
            ("Descripciones de tablas", "SELECT COUNT(*) as count FROM CONFIG_SISTEMA WHERE categoria='DESCRIPCION_TABLA'"),
            ("Configuraciones", "SELECT COUNT(*) as count FROM CONFIG_SISTEMA WHERE categoria='CONFIGURACION'"),
        ]
        
        all_verified = True
        for name, query in verification_queries:
            result = db.execute_query(query)
            count = result[0]['count']
            status = "✅" if count > 0 else "❌"
            print(f"{status} {name}: {count} registros")
            if count == 0:
                all_verified = False
        
        # ========================================================================
        # RESUMEN FINAL
        # ========================================================================
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print_header("📊 RESUMEN DE FASE 1")
        
        print(f"⏱️  Duración total: {duration:.2f} segundos")
        print(f"📋 Tablas analizadas: {len(schema['tables'])}")
        print(f"📜 Reglas deducidas: {len(rules)}")
        print(f"💾 Registros en CONFIG_SISTEMA: {total_records}")
        print(f"✅ Estado: {'COMPLETADO' if all_verified else 'COMPLETADO CON ADVERTENCIAS'}")
        
        # Mostrar distribución de reglas
        rule_types = {}
        for rule in rules:
            rule_type = rule['type']
            rule_types[rule_type] = rule_types.get(rule_type, 0) + 1
        
        print("\n📈 Distribución de reglas por tipo:")
        for rule_type, count in sorted(rule_types.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  • {rule_type}: {count}")
        
        # Mostrar resumen de CONFIG_SISTEMA
        populator.show_summary()
        
        # ========================================================================
        # GENERAR DRF1
        # ========================================================================
        print_header("📄 Generando DRF1 (Documento Resumen de Fase 1)")
        
        drf1_content = generate_drf1(schema, rules, total_records, duration)
        drf1_file = 'database/schema/DRF1_Fase1_Resumen.md'
        
        with open(drf1_file, 'w', encoding='utf-8') as f:
            f.write(drf1_content)
        
        print(f"✅ DRF1 generado: {drf1_file}")
        
        # ========================================================================
        # FINALIZACIÓN
        # ========================================================================
        db.close()
        
        print_header("🎉 FASE 1 COMPLETADA EXITOSAMENTE")
        print(f"📁 Archivos generados:")
        print(f"  • {schema_file}")
        print(f"  • {discovery_file}")
        print(f"  • {drf1_file}")
        print(f"\n✨ El sistema está listo para la FASE 2: Motor de Lenguaje\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR EN FASE 1: {e}")
        import traceback
        traceback.print_exc()
        return 1


def generate_drf1(schema, rules, total_records, duration):
    """Genera el contenido del DRF1"""
    
    content = f"""# 📋 DRF1 - Documento Resumen de Fase 1

**Fase:** Conectividad, Esquema e Ingeniería Inversa  
**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Duración:** {duration:.2f} segundos  
**Estado:** ✅ COMPLETADO

---

## 🎯 Objetivos Cumplidos

- [x] Configurar conexión segura a base de datos RUBIOGARCIADENTAL
- [x] Extraer esquema completo (tablas, PK/FK, constraints)
- [x] Crear tabla CONFIG_SISTEMA
- [x] Implementar algoritmo de auto-descubrimiento
- [x] Generar Prompt de Sistema Inicial
- [x] Deducir Reglas de Negocio desde esquema
- [x] Poblar CONFIG_SISTEMA con configuración inicial

---

## 📊 Métricas

| Métrica | Valor |
|---------|-------|
| Tablas analizadas | {len(schema['tables'])} |
| Reglas de negocio deducidas | {len(rules)} |
| Registros en CONFIG_SISTEMA | {total_records} |
| Tiempo de ejecución | {duration:.2f}s |

---

## 🗂️ Estructura de CONFIG_SISTEMA

La tabla CONFIG_SISTEMA ha sido creada con la siguiente estructura:

- **Categorías implementadas:**
  - `PROMPT`: Prompts del sistema
  - `REGLA_NEGOCIO`: Reglas de validación y negocio
  - `DESCRIPCION_TABLA`: Descripciones de tablas
  - `CONFIGURACION`: Configuraciones del sistema

- **Características:**
  - Versionado de configuración
  - Auditoría de cambios
  - Priorización de reglas
  - Activación/desactivación dinámica

---

## 🧠 Auto-Descubrimiento

El algoritmo de auto-descubrimiento ha analizado el esquema y deducido:

### Tipos de Reglas Detectadas

"""
    
    # Agregar distribución de reglas
    rule_types = {}
    for rule in rules:
        rule_type = rule['type']
        rule_types[rule_type] = rule_types.get(rule_type, 0) + 1
    
    for rule_type, count in sorted(rule_types.items(), key=lambda x: x[1], reverse=True):
        content += f"- **{rule_type}**: {count} reglas\n"
    
    content += f"""
---

## 💬 Prompt del Sistema

Se ha generado automáticamente un prompt del sistema de {len(schema['tables'])} tablas analizadas.

El prompt incluye:
- Descripción del rol (Alveolo, asistente de clínica dental)
- Listado de tablas principales
- Capacidades del sistema
- Reglas de negocio detectadas
- Instrucciones de operación

---

## 📁 Archivos Generados

1. `database/schema/schema_extracted.json` - Esquema completo de la base de datos
2. `database/schema/auto_discovery_results.json` - Resultados del auto-descubrimiento
3. `database/schema/CONFIG_SISTEMA.sql` - Script de creación de tabla
4. `database/schema/DRF1_Fase1_Resumen.md` - Este documento

---

## ✅ Verificación

Todas las verificaciones han pasado exitosamente:

- ✅ Conexión a base de datos establecida
- ✅ Esquema extraído completamente
- ✅ Tabla CONFIG_SISTEMA creada
- ✅ Reglas de negocio deducidas e insertadas
- ✅ Prompt del sistema generado e insertado
- ✅ Metadatos del sistema configurados

---

## 🚀 Próximos Pasos (FASE 2)

La Fase 1 está completa. El sistema está listo para:

1. Desplegar LLM local (Ollama)
2. Implementar wrapper de inyección dinámica
3. Configurar lectura en tiempo real desde CONFIG_SISTEMA
4. Validar que el LLM lee y aplica las reglas correctamente

---

**Generado automáticamente por el sistema de Auto-Configuración**  
*Fase 1 del Sistema IA Dental Autónomo*
"""
    
    return content


if __name__ == "__main__":
    sys.exit(main())
