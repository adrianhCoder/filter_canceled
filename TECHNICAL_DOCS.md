# Documentación Técnica - Módulo Filter Canceled

**Autor:** Adrianh De Lucio Chavero  
**Email:** adrianh_coder@outlook.com  
**Versión:** 17.0.1.0.0  
**Fecha:** Agosto 2025  
**Licencia:** LGPL-3

## Arquitectura del Módulo

### 1. Estructura de Archivos

```
filter_canceled/
├── __init__.py                          # Inicialización del módulo
├── __manifest__.py                      # Manifesto del módulo
├── README.md                           # Documentación del usuario
├── TECHNICAL_DOCS.md                   # Esta documentación técnica
├── models/
│   ├── __init__.py                     # Importación de modelos
│   └── account_report.py               # Extensión del modelo account.report
├── views/
│   └── account_report_view.xml         # Vista del formulario del reporte
├── static/
│   └── src/
│       ├── filter_canceled_assets.xml  # Assets del frontend
│       └── components/
│           └── account_report/
│               └── filters/
│                   ├── filter_hide_cancel_requested.js
│                   └── filter_hide_cancel_requested.xml
├── data/
│   └── ir_model_data.xml               # Datos de configuración
├── i18n/
│   └── es.po                           # Traducciones en español
├── tests/
│   ├── __init__.py                     # Importación de pruebas
│   └── test_filter_canceled.py         # Pruebas unitarias
└── scripts/
    ├── install_filter.py               # Script de instalación
    └── config.py                       # Configuración del script
```

### 2. Modelo Backend (Python)

#### 2.1 Extensión del Modelo account.report

```python
class AccountReport(models.Model):
    _inherit = 'account.report'
    
    filter_hide_cancel_requested = fields.Boolean(
        string="Ocultar en proceso cancelación",
        compute=lambda x: x._compute_report_option_filter('filter_hide_cancel_requested', False),
        readonly=False,
        store=True,
        depends=['root_report_id', 'section_main_report_ids'],
    )
```

#### 2.2 Métodos Clave

**Inicialización de Opciones:**
```python
def _init_options_hide_cancel_requested(self, options, previous_options=None):
    if self.filter_hide_cancel_requested and previous_options:
        options['hide_cancel_requested'] = previous_options.get('hide_cancel_requested', False)
    else:
        options['hide_cancel_requested'] = False
```

**Generación del Dominio:**
```python
@api.model
def _get_options_hide_cancel_requested_domain(self, options):
    if options.get('hide_cancel_requested'):
        return [('move_id.l10n_mx_edi_cfdi_state', '!=', 'cancel_requested')]
    return []
```

**Integración en el Sistema:**
```python
def _get_options_domain(self, options, date_scope):
    domain = super()._get_options_domain(options, date_scope)
    domain += self._get_options_hide_cancel_requested_domain(options)
    return domain
```

### 3. Frontend (JavaScript/XML)

#### 3.1 Componente JavaScript

```javascript
export class AccountReportFilterHideCancelRequested extends Component {
    static template = "filter_canceled.AccountReportFilterHideCancelRequested";
    static components = {
        DropdownItem,
    };

    setup() {
        this.controller = this.env.controller;
    }

    async toggleFilter(optionKey) {
        await this.controller.toggleOption(optionKey, true);
    }
}
```

#### 3.2 Template XML

```xml
<t t-name="filter_canceled.AccountReportFilterHideCancelRequested">
    <t t-if="controller.filters.show_hide_cancel_requested">
        <DropdownItem
            class="{ 'selected': controller.options.hide_cancel_requested }"
            onSelected="() => this.toggleFilter('hide_cancel_requested')"
        >
            Ocultar en proceso cancelación
        </DropdownItem>
    </t>
</t>
```

### 4. Flujo de Datos

#### 4.1 Inicialización del Reporte

1. **Carga del Reporte**: Se llama a `get_options()` en el modelo `account.report`
2. **Secuencia de Inicializadores**: Se ejecutan los métodos `_init_options_*` en orden
3. **Nuestro Inicializador**: `_init_options_hide_cancel_requested()` se ejecuta en la posición 785
4. **Configuración de Opciones**: Se establece `options['hide_cancel_requested'] = False`

#### 4.2 Aplicación del Filtro

1. **Consulta de Datos**: Se llama a `_query_get()` para obtener los datos del reporte
2. **Construcción del Dominio**: Se ejecuta `_get_options_domain()` que incluye nuestro filtro
3. **Nuestro Dominio**: `_get_options_hide_cancel_requested_domain()` genera el filtro SQL
4. **Aplicación**: Se aplica `('move_id.l10n_mx_edi_cfdi_state', '!=', 'cancel_requested')`

#### 4.3 Interacción del Usuario

1. **Clic en Filtro**: Usuario hace clic en "Ocultar en proceso cancelación"
2. **Toggle JavaScript**: Se ejecuta `toggleFilter('hide_cancel_requested')`
3. **Actualización de Opciones**: Se cambia `options.hide_cancel_requested = true`
4. **Recarga del Reporte**: Se recargan los datos con el nuevo filtro aplicado

### 5. Integración con el Sistema de Filtros

#### 5.1 Secuencia de Inicializadores

El módulo se integra en el sistema de filtros existente mediante:

```python
def _get_options_initializers_forced_sequence_map(self):
    sequence_map = super()._get_options_initializers_forced_sequence_map()
    sequence_map.update({
        self._init_options_hide_cancel_requested: 785,
    })
    return sequence_map
```

#### 5.2 Posición en la Secuencia

- **780**: `_init_options_reconciled` (filtro de asientos no conciliados)
- **785**: `_init_options_hide_cancel_requested` (nuestro filtro)
- **790**: `_init_options_account_type` (filtro de tipos de cuenta)

### 6. Filtro SQL Generado

Cuando el filtro está activo, se genera la siguiente consulta SQL:

```sql
SELECT ... FROM account_move_line 
WHERE ... 
  AND move_id.l10n_mx_edi_cfdi_state != 'cancel_requested'
```

### 7. Estados CFDI Soportados

El módulo filtra basándose en el campo `l10n_mx_edi_cfdi_state`:

| Estado | Descripción | Comportamiento |
|--------|-------------|----------------|
| `sent` | Firmado | ✅ Se muestra |
| `cancel_requested` | En proceso de cancelación | ❌ Se oculta |
| `cancel` | Cancelado | ✅ Se muestra |
| `received` | Recibido | ✅ Se muestra |
| `global_sent` | Global firmado | ✅ Se muestra |
| `global_cancel` | Global cancelado | ✅ Se muestra |

### 8. Pruebas Unitarias

Las pruebas cubren:

1. **Creación del Campo**: Verifica que el campo se crea correctamente
2. **Inicialización**: Prueba la inicialización de opciones
3. **Generación de Dominio**: Verifica la generación correcta del filtro SQL
4. **Integración**: Prueba que el filtro se integra correctamente en el sistema
5. **Secuencia**: Verifica que el filtro está en la posición correcta

### 9. Configuración y Personalización

#### 9.1 Habilitar en Reportes Específicos

```python
# En el script de instalación
report_names = [
    'Aged Partner Balance',
    'General Ledger',
    'Trial Balance',
    'Partner Ledger',
]

for report_name in report_names:
    report = env['account.report'].search([('name', '=', report_name)], limit=1)
    if report:
        report.filter_hide_cancel_requested = True
```

#### 9.2 Personalizar el Dominio

Para modificar qué estados se ocultan:

```python
@api.model
def _get_options_hide_cancel_requested_domain(self, options):
    if options.get('hide_cancel_requested'):
        # Ocultar múltiples estados
        return [('move_id.l10n_mx_edi_cfdi_state', 'not in', ['cancel_requested', 'cancel'])]
    return []
```

### 10. Consideraciones de Rendimiento

1. **Índice Recomendado**: Se recomienda crear un índice en `l10n_mx_edi_cfdi_state`
2. **Filtro Eficiente**: El filtro usa una condición simple de desigualdad
3. **Caché**: Las opciones se almacenan en la sesión del navegador

### 11. Compatibilidad

- **Odoo 17.0+**: Desarrollado y probado en Odoo 17
- **Módulos Requeridos**: `account`, `account_reports`, `l10n_mx_edi`
- **Base de Datos**: Compatible con bases de datos existentes
- **Módulos Personalizados**: No interfiere con otros módulos

### 12. Mantenimiento

#### 12.1 Actualizaciones

Para actualizar el módulo:

1. Actualizar el código
2. Ejecutar `-u filter_canceled` en Odoo
3. Verificar que las pruebas pasen

#### 12.2 Debugging

Para debuggear problemas:

1. Verificar logs de Odoo
2. Revisar la consola del navegador
3. Ejecutar las pruebas unitarias
4. Verificar la configuración del reporte

### 13. Extensibilidad

El módulo está diseñado para ser extensible:

1. **Nuevos Estados**: Fácil agregar nuevos estados CFDI
2. **Nuevos Filtros**: El patrón se puede replicar para otros filtros
3. **Personalización**: Fácil modificar el comportamiento del filtro
