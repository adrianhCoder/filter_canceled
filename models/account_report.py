# -*- coding: utf-8 -*-
"""
Módulo Filter Canceled - Filtro para ocultar facturas en proceso de cancelación
Autor: Adrianh De Lucio Chavero
Email: adrianh_coder@outlook.com
Versión: 17.0.1.0.0
"""

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountReport(models.Model):
    _inherit = 'account.report'

    # Campo para habilitar/deshabilitar el filtro de cancelación
    filter_hide_cancel_requested = fields.Boolean(
        string="Ocultar en proceso cancelación",
        compute=lambda x: x._compute_report_option_filter('filter_hide_cancel_requested', False),
        readonly=False,
        store=True,
        depends=['root_report_id', 'section_main_report_ids'],
    )

    ####################################################
    # OPTIONS: hide canceled requested entries
    ####################################################
    def _init_options_hide_cancel_requested(self, options, previous_options=None):
        """
        Inicializa la opción para ocultar facturas en proceso de cancelación.
        """
        import logging
        _logger = logging.getLogger(__name__)
        
        _logger.info(f"Initializing hide cancel requested options. Filter enabled: {self.filter_hide_cancel_requested}")
        _logger.info(f"Previous options: {previous_options}")
        
        if self.filter_hide_cancel_requested:
            # Por defecto, activar el filtro cuando está habilitado en el reporte
            # El usuario puede desactivarlo manualmente si lo desea
            options['hide_cancel_requested'] = True
            _logger.info("Filter enabled in report, setting to True by default")
        else:
            options['hide_cancel_requested'] = False
            _logger.info("Filter not enabled in report, setting to False")
            
        _logger.info(f"Hide cancel requested option set to: {options['hide_cancel_requested']}")

    @api.model
    def _get_options_hide_cancel_requested_domain(self, options):
        """
        Genera el dominio para ocultar facturas en proceso de cancelación.
        """
        import logging
        _logger = logging.getLogger(__name__)
        
        _logger.info(f"Hide cancel requested domain called with options: {options.get('hide_cancel_requested')}")
        
        if options.get('hide_cancel_requested'):
            if 'l10n_mx_edi_cfdi_state' in self.env['account.move']._fields:
                domain = [('move_id.l10n_mx_edi_cfdi_state', '!=', 'cancel_requested')]
                _logger.info(f"Applying hide cancel requested domain: {domain}")
                return domain
            else:
                _logger.info("Field l10n_mx_edi_cfdi_state not found, skipping filter")
        return []

    def _get_options_initializers_forced_sequence_map(self):
        """
        Extiende el mapa de secuencia para incluir nuestro nuevo filtro.
        """
        sequence_map = super()._get_options_initializers_forced_sequence_map()
        
        # Agregar nuestro filtro después del filtro de asientos no conciliados
        sequence_map.update({
            self._init_options_hide_cancel_requested: 785,  # Después de _init_options_reconciled (780)
        })
        
        return sequence_map

    def _get_options_domain(self, options, date_scope):
        """
        Extiende el dominio para incluir nuestro filtro de cancelación.
        """
        domain = super()._get_options_domain(options, date_scope)
        domain += self._get_options_hide_cancel_requested_domain(options)
        return domain


