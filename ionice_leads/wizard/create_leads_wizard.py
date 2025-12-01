from odoo import models, fields, api


class CreateLeadsWizard(models.TransientModel):
    _name = 'create.leads.wizard'
    _description = 'Wizard para crear leads desde contactos'

    partner_ids = fields.Many2many('res.partner', string='Contactos')

    @api.model
    def default_get(self, fields_list):
        """Obtener los contactos seleccionados del contexto"""
        res = super().default_get(fields_list)
        if self.env.context.get('active_model') == 'res.partner' and self.env.context.get('active_ids'):
            res['partner_ids'] = [(6, 0, self.env.context.get('active_ids', []))]
        return res

    def action_create_leads(self):
        """Crear leads desde los contactos seleccionados"""
        CrmTag = self.env['crm.tag']
        CrmLead = self.env['crm.lead']

        leads_creados = 0
        leads_existentes = 0

        for partner in self.partner_ids:
            # Verificar si ya existe un lead para este contacto
            existing_lead = CrmLead.search([
                ('partner_id', '=', partner.id),
                ('type', '=', 'lead')
            ], limit=1)

            if existing_lead:
                leads_existentes += 1
                continue

            # Obtener o crear etiquetas CRM basadas en las etiquetas del contacto
            crm_tag_ids = []
            for category in partner.category_id:
                # Buscar si existe una etiqueta CRM con el mismo nombre
                crm_tag = CrmTag.search([('name', '=', category.name)], limit=1)
                if not crm_tag:
                    # Si no existe, crearla
                    crm_tag = CrmTag.create({'name': category.name})
                crm_tag_ids.append(crm_tag.id)

            # Crear el lead (no oportunidad)
            CrmLead.create({
                'name': partner.name,
                'partner_id': partner.id,
                'type': 'lead',
                'tag_ids': [(6, 0, crm_tag_ids)] if crm_tag_ids else False,
            })
            leads_creados += 1

        # Mostrar mensaje de éxito con detalles
        mensaje = f'Se crearon {leads_creados} leads correctamente.'
        if leads_existentes > 0:
            mensaje += f' {leads_existentes} contacto(s) ya tenían un lead asociado.'

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Proceso completado',
                'message': mensaje,
                'type': 'success',
                'sticky': False,
            }
        }

