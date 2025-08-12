# -*- coding: utf-8 -*-
"""
Pruebas unitarias para el módulo Filter Canceled
Autor: Adrianh De Lucio Chavero
Email: adrianh_coder@outlook.com
"""

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestFilterCanceled(TransactionCase):

    def setUp(self):
        super().setUp()
        self.report = self.env['account.report'].create({
            'name': 'Test Report',
            'root_report_id': False,
        })

    def test_filter_hide_cancel_requested_field(self):
        """Test that the filter_hide_cancel_requested field is properly created"""
        self.assertTrue(hasattr(self.report, 'filter_hide_cancel_requested'))
        self.assertIsInstance(self.report.filter_hide_cancel_requested, bool)

    def test_init_options_hide_cancel_requested(self):
        """Test the initialization of the hide_cancel_requested option"""
        options = {}
        previous_options = {'hide_cancel_requested': True}
        
        # Test with filter enabled and previous options
        self.report.filter_hide_cancel_requested = True
        self.report._init_options_hide_cancel_requested(options, previous_options)
        self.assertTrue(options.get('hide_cancel_requested'))
        
        # Test with filter disabled
        options = {}
        self.report.filter_hide_cancel_requested = False
        self.report._init_options_hide_cancel_requested(options, previous_options)
        self.assertFalse(options.get('hide_cancel_requested'))

    def test_get_options_hide_cancel_requested_domain(self):
        """Test the domain generation for the hide_cancel_requested filter"""
        # Test when filter is active
        options = {'hide_cancel_requested': True}
        domain = self.report._get_options_hide_cancel_requested_domain(options)
        expected_domain = [('move_id.l10n_mx_edi_cfdi_state', '!=', 'cancel_requested')]
        self.assertEqual(domain, expected_domain)
        
        # Test when filter is inactive
        options = {'hide_cancel_requested': False}
        domain = self.report._get_options_hide_cancel_requested_domain(options)
        self.assertEqual(domain, [])

    def test_get_options_domain_integration(self):
        """Test that the hide_cancel_requested domain is properly integrated"""
        options = {'hide_cancel_requested': True}
        base_domain = [('display_type', 'not in', ('line_section', 'line_note'))]
        
        # Mock the parent method to return base domain
        original_get_options_domain = self.report._get_options_domain
        def mock_get_options_domain(options, date_scope):
            return base_domain
        
        self.report._get_options_domain = mock_get_options_domain
        
        # Test that our domain is added to the base domain
        result_domain = self.report._get_options_domain(options, 'normal')
        expected_domain = base_domain + [('move_id.l10n_mx_edi_cfdi_state', '!=', 'cancel_requested')]
        self.assertEqual(result_domain, expected_domain)
        
        # Restore original method
        self.report._get_options_domain = original_get_options_domain

    def test_sequence_map_integration(self):
        """Test that our filter is properly integrated into the sequence map"""
        sequence_map = self.report._get_options_initializers_forced_sequence_map()
        
        # Check that our method is in the sequence map
        self.assertIn(self.report._init_options_hide_cancel_requested, sequence_map)
        
        # Check that our sequence number is reasonable (after _init_options_reconciled)
        our_sequence = sequence_map[self.report._init_options_hide_cancel_requested]
        self.assertEqual(our_sequence, 785)
