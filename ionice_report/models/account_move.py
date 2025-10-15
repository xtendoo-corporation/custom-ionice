# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Puedes agregar campos personalizados aquí si los necesitas
    # Por ejemplo:
    # ionice_custom_field = fields.Char(string='Campo Personalizado')
