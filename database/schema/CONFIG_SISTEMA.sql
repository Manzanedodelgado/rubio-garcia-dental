-- ============================================================================
-- FASE 1 - TABLA CONFIG_SISTEMA
-- Tabla de auto-configuración del sistema de IA
-- ============================================================================

-- Eliminar tabla si existe (solo para desarrollo)
IF OBJECT_ID('CONFIG_SISTEMA', 'U') IS NOT NULL
    DROP TABLE CONFIG_SISTEMA;
GO

-- Crear tabla CONFIG_SISTEMA
CREATE TABLE CONFIG_SISTEMA (
    id INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Clasificación
    categoria VARCHAR(50) NOT NULL,  -- 'PROMPT', 'REGLA_NEGOCIO', 'VALIDACION', 'CONFIGURACION'
    clave VARCHAR(100) NOT NULL,
    
    -- Valor y metadatos
    valor NVARCHAR(MAX) NOT NULL,
    tipo_dato VARCHAR(20) NOT NULL,  -- 'TEXT', 'JSON', 'NUMBER', 'BOOLEAN'
    
    -- Control de activación
    activo BIT DEFAULT 1,
    prioridad INT DEFAULT 100,  -- Menor número = mayor prioridad
    
    -- Versionado y auditoría
    version INT DEFAULT 1,
    fecha_creacion DATETIME DEFAULT GETDATE(),
    fecha_modificacion DATETIME DEFAULT GETDATE(),
    modificado_por VARCHAR(100),  -- 'SISTEMA', 'USUARIO', 'AUTO_REFLEXION'
    razon_cambio NVARCHAR(500),
    
    -- Constraint de unicidad
    CONSTRAINT UQ_CONFIG_CATEGORIA_CLAVE UNIQUE(categoria, clave)
);
GO

-- Índices para optimizar búsquedas
CREATE INDEX idx_config_categoria ON CONFIG_SISTEMA(categoria, activo);
CREATE INDEX idx_config_prioridad ON CONFIG_SISTEMA(prioridad DESC);
CREATE INDEX idx_config_fecha_mod ON CONFIG_SISTEMA(fecha_modificacion DESC);
GO

-- Comentarios de documentación
EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Tabla de auto-configuración del sistema de IA. Almacena prompts, reglas de negocio y validaciones que se leen dinámicamente.', 
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE',  @level1name = N'CONFIG_SISTEMA';
GO

PRINT '✅ Tabla CONFIG_SISTEMA creada exitosamente';
GO
