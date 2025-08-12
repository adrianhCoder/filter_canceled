# Configuración para el script de instalación del filtro de cancelación

# Configuración de la base de datos
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 8069,
    'database': 'your_database_name',  # Cambiar por el nombre de tu base de datos
    'user': 'admin',
    'password': 'admin',
}

# Reportes donde habilitar el filtro por defecto
DEFAULT_REPORTS = [
    'Aged Partner Balance',      # Antigüedad de saldos
    'General Ledger',            # Libro mayor
    'Trial Balance',             # Balance de comprobación
    'Partner Ledger',            # Mayor de clientes
    'Account Follow-up',         # Seguimiento de cuentas
    'Bank Reconciliation',       # Conciliación bancaria
]

# Configuración del filtro
FILTER_CONFIG = {
    'enabled_by_default': True,  # Si el filtro debe estar habilitado por defecto
    'show_in_ui': True,          # Si el filtro debe aparecer en la interfaz
    'help_text': 'Oculta todas las facturas que están en proceso de cancelación CFDI',
}
