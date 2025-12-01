from odoo import models, fields, api


class ScheduleActivityWizard(models.TransientModel):
    _name = 'schedule.activity.wizard'
    _description = 'Wizard para programar actividades en leads'

    lead_ids = fields.Many2many('crm.lead', string='Leads')
    lead_count = fields.Integer(string='Número de Leads', compute='_compute_lead_count')
    activity_type_id = fields.Many2one('mail.activity.type', string='Tipo de Actividad', required=True)
    summary = fields.Char(string='Resumen')
    note = fields.Html(string='Nota')
    date_deadline = fields.Date(string='Fecha límite', required=True, default=fields.Date.context_today)
    user_id = fields.Many2one('res.users', string='Asignado a', required=True, default=lambda self: self.env.user)

    @api.depends('lead_ids')
    def _compute_lead_count(self):
        """Calcular el número de leads seleccionados"""
        for wizard in self:
            wizard.lead_count = len(wizard.lead_ids)

    @api.model
    def default_get(self, fields_list):
        """Obtener los leads seleccionados del contexto"""
        res = super().default_get(fields_list)
        if self.env.context.get('active_model') == 'crm.lead' and self.env.context.get('active_ids'):
            res['lead_ids'] = [(6, 0, self.env.context.get('active_ids', []))]
        return res

    def action_schedule_activities(self):
        """Programar actividades para los leads seleccionados"""
        total_leads = len(self.lead_ids)
        actividades_creadas = 0

        for index, lead in enumerate(self.lead_ids, start=1):
            # Crear la actividad para este lead
            self.env['mail.activity'].create({
                'activity_type_id': self.activity_type_id.id,
                'summary': self.summary or self.activity_type_id.name,
                'note': self.note,
                'date_deadline': self.date_deadline,
                'user_id': self.user_id.id,
                'res_model_id': self.env['ir.model']._get('crm.lead').id,
                'res_id': lead.id,
            })
            actividades_creadas += 1

            # Mostrar notificación de progreso cada 5 leads o en el último
            if index % 5 == 0 or index == total_leads:
                self.env['bus.bus']._sendone(
                    self.env.user.partner_id,
                    'simple_notification',
                    {
                        'title': 'Programando actividades',
                        'message': f'Procesando lead {index} de {total_leads}: {lead.name}',
                        'type': 'info',
                        'sticky': False,
                    }
                )

        # Mostrar mensaje final de éxito
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Actividades programadas',
                'message': f'Se programaron {actividades_creadas} actividades correctamente en {total_leads} leads.',
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

