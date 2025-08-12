# Módulo Filter Canceled

**Autor:** Adrianh De Lucio Chavero  
**Email:** adrianh_coder@outlook.com  
**Versión:** 17.0.1.0.0  
**Licencia:** LGPL-3

## Descripción

Este módulo agrega un filtro adicional en los reportes contables de Odoo 17 que permite ocultar todas las facturas que están en proceso de cancelación CFDI.

## Características

- **Filtro "Ocultar en proceso cancelación"**: Se agrega automáticamente a los reportes contables
- **Filtrado inteligente**: Oculta facturas con `l10n_mx_edi_cfdi_state = 'cancel_requested'`
- **Integración completa**: Compatible con el sistema de filtros existente de Odoo
- **Interfaz intuitiva**: Aparece en el menú desplegable de opciones de los reportes

## Instalación

1. Copia el módulo `filter_canceled` al directorio `addons` de tu instalación de Odoo
2. Actualiza la lista de aplicaciones en Odoo
3. Instala el módulo "Filtro para Ocultar Facturas en Proceso de Cancelación"

## Uso

### Configuración del Reporte

1. Ve a **Contabilidad > Configuración > Reportes**
2. Selecciona el reporte que deseas configurar
3. En la pestaña **Opciones**, busca la nueva sección con el campo **"Ocultar en proceso cancelación"**
4. Marca la casilla para habilitar el filtro
5. Guarda los cambios

### Uso del Filtro

1. Abre cualquier reporte contable (ej: Antigüedad de saldos, Libro mayor, etc.)
2. El filtro se aplica automáticamente cuando está habilitado en la configuración del reporte
3. Las facturas con estado CFDI 'cancel_requested' se ocultarán automáticamente
4. No necesitas hacer nada adicional en la interfaz del reporte

## Dependencias

- `account`: Módulo base de contabilidad
- `account_reports`: Sistema de reportes contables
- `l10n_mx_edi`: Módulo de facturación electrónica mexicana (opcional, para acceder al campo CFDI)

## Estructura del Módulo

```
filter_canceled/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   └── account_report.py
├── views/
│   └── account_report_view.xml
├── data/
│   └── ir_model_data.xml
├── i18n/
│   └── es.po
├── tests/
│   ├── __init__.py
│   └── test_filter_canceled.py
└── scripts/
    ├── install_filter.py
    └── config.py
```

## Funcionamiento Técnico

### Backend (Python)

1. **Campo del modelo**: Se agrega `filter_hide_cancel_requested` al modelo `account.report`
2. **Inicialización**: `_init_options_hide_cancel_requested()` inicializa la opción del filtro
3. **Dominio**: `_get_options_hide_cancel_requested_domain()` genera el filtro SQL
4. **Integración**: Se extiende `_get_options_domain()` para aplicar el filtro

### Frontend (Vista XML)

1. **Vista del formulario**: Se agrega el campo de configuración en la pestaña "Opciones"
2. **Integración**: Se integra con el sistema de filtros existente de Odoo
3. **Configuración**: El filtro se activa/desactiva desde la configuración del reporte

### Filtro SQL

Cuando el filtro está activo y el módulo `l10n_mx_edi` está instalado, se aplica la siguiente condición:
```sql
move_id.l10n_mx_edi_cfdi_state != 'cancel_requested'
```

Si el módulo `l10n_mx_edi` no está instalado, el filtro no se aplica (no hay error).

## Estados CFDI

El módulo filtra basándose en el campo `l10n_mx_edi_cfdi_state` del modelo `account.move`:

- `sent` - Firmado
- `cancel_requested` - **En proceso de cancelación** (se oculta)
- `cancel` - Cancelado
- `received` - Recibido
- `global_sent` - Global firmado
- `global_cancel` - Global cancelado

## Personalización

Para personalizar el comportamiento del filtro, puedes:

1. **Modificar el dominio**: Edita el método `_get_options_hide_cancel_requested_domain()` en `models/account_report.py`
2. **Cambiar el texto**: Modifica las traducciones en los archivos `.po`
3. **Agregar más estados**: Extiende la lógica para incluir otros estados CFDI

## Soporte

Para reportar problemas o solicitar mejoras, contacta al equipo de desarrollo.

## Licencia

Este módulo está bajo la licencia LGPL-3.
