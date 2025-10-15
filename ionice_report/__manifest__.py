# -*- coding: utf-8 -*-
{
    'name': 'Ionice - Formato de Facturas y Presupuestos',
    'version': '18.0.1.0.0',
    'summary': 'Formato personalizado de facturas y presupuestos para Ionice',
    'description': """
        Módulo para personalizar el formato de impresión de facturas y presupuestos de Ionice

        Características:
        * Diseño personalizado de facturas
        * Diseño personalizado de presupuestos
        * Logo y datos de empresa
        * Formato profesional
    """,
    'author': 'custom-ionice',
    'website': 'https://www.ionice.es',
    'category': 'Accounting/Accounting',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'sale',
        'base',
    ],
    'data': [
        'views/report_invoice.xml',
        'views/report_sale_order.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
