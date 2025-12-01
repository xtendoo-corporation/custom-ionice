{
    'name': 'Ionice Leads',
    'version': '1.0.0',
    'category': 'CRM',
    'summary': 'Acción para crear leads desde contactos',
    'description': 'Permite seleccionar varios contactos y crear leads en CRM con el nombre y etiqueta del contacto.',
    'author': 'xtendoo',
    'depends': ['base', 'crm', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/create_leads_wizard.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

