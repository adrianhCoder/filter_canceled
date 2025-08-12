{
    'name': 'Filtro para Ocultar Facturas en Proceso de Cancelación',
    'version': '17.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Agrega un filtro para ocultar facturas en proceso de cancelación en reportes contables',
    'description': """
        Este módulo agrega un filtro adicional en los reportes contables que permite ocultar
        todas las facturas que tienen el estado CFDI 'cancel_requested' (en proceso de cancelación).
        
        Características:
        - Filtro "Ocultar en proceso cancelación" en reportes contables
        - Oculta facturas con l10n_mx_edi_cfdi_state = 'cancel_requested' (si l10n_mx_edi está instalado)
        - Compatible con el sistema de filtros existente de Odoo
        - Funciona incluso si l10n_mx_edi no está instalado (filtro inactivo)
    """,
    'author': 'Adrianh De Lucio Chavero',
    'website': 'https://github.com/adrianh-coder',
    'email': 'adrianh_coder@outlook.com',
    'depends': [
        'account',
        'account_reports',
    ],
    'data': [
        'data/ir_model_data.xml',
        'views/account_report_view.xml',
    ],
    'test': [
        'tests/test_filter_canceled.py',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
