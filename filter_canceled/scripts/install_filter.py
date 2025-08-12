#!/usr/bin/env python3
"""
Script para instalar y configurar el filtro de cancelación en reportes existentes.
Este script debe ejecutarse después de instalar el módulo filter_canceled.
"""

import sys
import os

# Agregar el directorio raíz de Odoo al path
sys.path.append('/path/to/odoo')  # Cambiar por la ruta real de Odoo

import odoo
from odoo import api, SUPERUSER_ID


def install_filter_on_reports():
    """
    Habilita el filtro de cancelación en reportes específicos.
    """
    # Inicializar Odoo
    odoo.cli.server.main()
    
    # Obtener el entorno
    env = api.Environment(odoo.registry('your_database'), SUPERUSER_ID, {})
    
    # Lista de reportes donde habilitar el filtro
    report_names = [
        'Aged Partner Balance',  # Antigüedad de saldos
        'General Ledger',        # Libro mayor
        'Trial Balance',         # Balance de comprobación
        'Partner Ledger',        # Mayor de clientes
    ]
    
    # Habilitar el filtro en los reportes especificados
    for report_name in report_names:
        report = env['account.report'].search([('name', '=', report_name)], limit=1)
        if report:
            report.filter_hide_cancel_requested = True
            print(f"✅ Filtro habilitado en: {report_name}")
        else:
            print(f"⚠️  Reporte no encontrado: {report_name}")
    
    print("\n🎉 Instalación completada!")
    print("El filtro 'Ocultar en proceso cancelación' está ahora disponible en los reportes configurados.")


if __name__ == "__main__":
    print("Instalando filtro de cancelación en reportes...")
    install_filter_on_reports()
